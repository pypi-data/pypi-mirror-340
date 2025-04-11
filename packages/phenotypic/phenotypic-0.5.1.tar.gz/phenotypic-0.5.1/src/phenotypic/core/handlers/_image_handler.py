from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING: from phenotypic import Image

import uuid
from typing import Optional, Union, Dict, Tuple
import numpy as np
import skimage as ski
import matplotlib.pyplot as plt
from os import PathLike
from pathlib import Path
import warnings

from skimage.color import rgb2gray, rgba2rgb
from skimage.transform import rotate as skimage_rotate
from scipy.ndimage import rotate as scipy_rotate
from copy import deepcopy
from typing import Type

from scipy.sparse import csc_matrix

from ..accessors import (
    ImageArray,
    ImageMatrix,
    ImageEnhancedMatrix,
    ObjectMask,
    ObjectMap,
    ImageObjects
)

from phenotypic.util.constants_ import IMAGE_FORMATS, METADATA_LABELS
from phenotypic.util.exceptions_ import (
    EmptyImageError, NoArrayError, NoObjectsError, IllegalAssignmentError,
    UnsupportedSchemaError, UnsupportedFileTypeError
)


class ImageHandler:
    """The core comprehensive class for handling image processing, including manipulation, information sync, metadata management, and format conversion.

    The `ImageHandler` class is designed to load, process, and manage image data using different
    representation formats (e.g., arrays and matrices). This class allows for metadata editing,
    schema definition, and subcomponent handling to streamline image processing tasks.

    Note:
        If the input_image is 2-D, the ImageHandler leave the array form as None
        If the input_image is 3-D, the ImageHandler will automatically set the matrix component to the grayscale representation.

    Attributes:
        _array (Optional[np.ndarray]): The numeric array representation of the image
            used for multichannel data processing.
        _matrix (Optional[np.ndarray]): The matrix representation of the image, primarily
            used for 2D image data or grayscale formats.
        _enh_matrix (Optional[np.ndarray]): A detection matrix representation, useful for
            object detection tasks and similar applications.
        _sparse_object_map (Optional[csc_matrix]): A sparse object map for efficient
            representation of object detection overlays.
        __image_format (Optional[str]): A schema defining the format of the image input,
            influencing how data is interpreted or manipulated.
        _private_metadata (Dict[str, Any]): Immutable metadata associated with the image,
            including a universally unique identifier (UUID).
        _protected_metadata (Dict[str, Optional[Union[int, float, str, bool, np.integer,
            np.floating, np.complexfloating]]]): Editable protected metadata,
            such as the image name, providing key image-related information.
        _public_metadata (Dict[str, Union[int, float, str, bool, np.integer, np.floating,
            np.complexfloating]]): Public metadata that can be fully edited or
            removed without restrictions.
        __array_subhandler (ImageArray): Subhandler responsible for array-based operations.
            Extends functionality for working with image arrays.
        __matrix_accessor (ImageMatrix): Subhandler for performing operations on the image
            matrix representation.
        __enh_matrix_accessor (ImageDetectionMatrix): Subhandler for handling detection
            matrix operations.
        __object_mask_subhandler (ObjectMask): Subhandler for managing object masks in the
            image.
        __object_map_subhandler (ObjectMap): Subhandler for working with object maps.
        __objects_subhandler (ImageObjects): Subhandler for managing objects detected in
            the image.
    """

    def __init__(self,
                 input_image: None | Union[np.ndarray, Image, PathLike] = None,
                 imformat: None | str = None,
                 name: Optional[str] = None):
        """
        Args:
            input_image: An optional input image represented as either a NumPy array or an image
                object. Defaults to None.
            imformat: An optional string defining the schema for the input image to specify
                how data should be interpreted or processed. Defaults to None.
            name: An optional string to assign a name to the image, used as metadata. If not
                provided, a universally unique identifier (UUID) will be generated and assigned.
        """
        self._array: Optional[np.ndarray] = None
        self._matrix: Optional[np.ndarray] = None
        self._enh_matrix: Optional[np.ndarray] = None
        self._sparse_object_map: Optional[csc_matrix] = None

        # Initialize core backend variables
        self.__image_format = None

        # Private metadata cannot be edited and is not duplicated with copies of the class
        self._private_metadata = {
            METADATA_LABELS.UUID: uuid.uuid4()
        }

        # Protected Metadata can be edited, but not removed
        self._protected_metadata: Dict[
            str, Optional[Union[int, float, str, bool, np.integer, np.floating, np.bool_, np.complexfloating]]
        ] = {
            METADATA_LABELS.IMAGE_NAME: name if name is not None else self._private_metadata[METADATA_LABELS.UUID],
        }

        # Public metadata can be edited or removed
        self._public_metadata: Dict[str, Union[int, float, str, bool, np.integer, np.floating, np.bool_, np.complexfloating]] = {}

        # Initialize image component handlers
        self.__array_subhandler: ImageArray = ImageArray(self)
        self.__matrix_accessor: ImageMatrix = ImageMatrix(self)
        self.__enh_matrix_accessor: ImageEnhancedMatrix = ImageEnhancedMatrix(self)
        self.__object_mask_subhandler: ObjectMask = ObjectMask(self)
        self.__object_map_subhandler: ObjectMap = ObjectMap(self)
        self.__objects_subhandler: ImageObjects = ImageObjects(self)

        if isinstance(input_image, (PathLike, str, Path)):
            self.imread(input_image)
        else:
            self.set_image(input_image=input_image, imformat=imformat)

    def __getitem__(self, key) -> Image:
        """Returns a subimage from the current object based on the provided key. The subimage is initialized
        as a new instance of the same class, maintaining the schema and format consistency as the original
        image object. This method supports 2-dimensional slicing and indexing.

        Args:
            key: A slicing key or index used to extract a subset or part of the image object.

        Returns:
            Image: An instance of the Image representing the subimage corresponding to the provided key.

        Raises:
            KeyError: If the provided key does not match the expected slicing format or dimensions.
        """
        if self.imformat not in IMAGE_FORMATS.MATRIX_FORMATS:
            subimage = self.__class__(input_image=self.array[key], imformat=self.imformat)
        else:
            subimage = self.__class__(input_image=self.matrix[key], imformat=self.imformat)

        subimage.enh_matrix[:] = self.enh_matrix[key]
        subimage.objmap[:] = self.objmap[key]
        return subimage

    def __setitem__(self, key, value):
        """Sets an item in the object with a given key and Image object. Ensures that the Image being set matches the expected shape and type, and updates internal properties accordingly.

        Args:
            key (Any): The array slices for accesssing the elements of the image.
            value (ImageHandler): The value to be set, which must match the shape of the
                existing elements and conform to the expected schema.

        Raises:
            ValueError: If the shape of the `value` does not match the shape of the existing
                elements being accessed.
        """
        if np.array_equal(self.shape, value.shape) is False: raise ValueError(
            'The image being set must be of the same shape as the image elements being accessed.'
        )
        if isinstance(value, ImageHandler) or issubclass(type(value), ImageHandler):
            if value.imformat not in IMAGE_FORMATS.MATRIX_FORMATS and self.imformat not in IMAGE_FORMATS.MATRIX_FORMATS:
                self._array[key] = value.array[:]
            self._matrix[key] = value.matrix[:]
            self._enh_matrix[key] = value.enh_matrix[:]
            self.objmask[key] = value.objmask[:]

    def __eq__(self, other) -> bool:
        return True if (
                self.imformat == other.imformat
                and np.array_equal(self.array[:], other.array[:])
                and np.array_equal(self.matrix[:], other.matrix[:])
                and np.array_equal(self.enh_matrix[:], other.enh_matrix[:])
                and np.array_equal(self.objmap[:], other.objmap[:])
                and self._protected_metadata == other._protected_metadata
                and self._public_metadata == other._public_metadata
        ) else False

    def __ne__(self, other):
        return not self == other

    def isempty(self) -> bool:
        """Returns True if there is no image data"""
        return True if self._matrix is None else False

    @property
    def name(self):
        """Returns the name of the image. If no name is set, the name will be the file stem of the image."""
        return self._protected_metadata[METADATA_LABELS.IMAGE_NAME]

    @name.setter
    def name(self, value):
        if type(value) != str:
            raise ValueError('Image name must be a string')
        self._protected_metadata[METADATA_LABELS.IMAGE_NAME] = value

    @property
    def uuid(self):
        """Returns the UUID of the image"""
        return self._private_metadata[METADATA_LABELS.UUID]

    @property
    def shape(self):
        """Returns the shape of the image array or matrix depending on input format or none if no image is set.

        Returns:
            Optional[Tuple(int,int,...)]: Returns the shape of the array or matrix depending on input format or none if no image is set.
        """
        if self._array is not None:
            return self._array.shape
        elif self._matrix is not None:
            return self._matrix.shape
        else:
            raise EmptyImageError

    @property
    def imformat(self) -> Optional[str]:
        """Returns the input format of the image array or matrix depending on input format"""
        if self.__image_format:
            return self.__image_format
        else:
            raise EmptyImageError

    @property
    def array(self) -> ImageArray:
        """Returns the ImageArray accessor; An image array represents the multichannel information

        Note:
            - array/matrix element data is synced
            - change image shape by changing the image being represented with Image.set_image()
            - Raises an error if input image has no array form

        Returns:
            ImageArray: A class that can be accessed like a numpy array, but has extra methods to streamline development, or None if not set

        Raises:
            NoArrayError: If no multichannel image data is set as input.
        See Also: :class:`ImageArray`
        """
        if self._array is None:
            if self._matrix is None:
                raise EmptyImageError
            else:
                raise NoArrayError
        else:
            return self.__array_subhandler

    @array.setter
    def array(self, value):
        if isinstance(value, np.ndarray) | value in {int, float, bool}:
            self.array[:] = value
        else:
            raise IllegalAssignmentError('array')

    @property
    def matrix(self) -> ImageMatrix:
        """The image's matrix representation. The array form is converted into a matrix form since some algorithm's only handle 2-D

        Note:
            - matrix elements are not directly mutable in order to preserve image information integrity
            - Change matrix elements by changing the image being represented with Image.set_image()

        Returns:
            ImageMatrix: An immutable container for the image matrix that can be accessed like a numpy array, but has extra methods to streamline development.

        See Also: :class:`ImageMatrix`
        """
        if self._matrix is None:
            raise EmptyImageError
        else:
            return self.__matrix_accessor

    @matrix.setter
    def matrix(self, value):
        if isinstance(value, np.ndarray) | value in {int, float, bool}:
            self.matrix[:] = value
        else:
            raise IllegalAssignmentError('matrix')

    @property
    def enh_matrix(self) -> ImageEnhancedMatrix:
        """Returns the image's enhanced matrix accessor (See: :class:`ImageEnhancedMatrix`. Preprocessing steps can be applied to this component to improve detection performance.

        The enhanceable matrix is a copy of the image's matrix form that can be modified and used to improve detection performance.
        The original matrix data should be left intact in order to preserve image information integrity for measurements.'

        Returns:
            ImageEnhancedMatrix: A mutable container that stores a copy of the image's matrix form

        See Also: :class:`ImageEnhancedMatrix`
        """
        if self._enh_matrix is None:
            raise EmptyImageError
        else:
            return self.__enh_matrix_accessor

    @enh_matrix.setter
    def enh_matrix(self, value):
        if isinstance(value, np.ndarray) | type(value) in {int, float, bool}:
            self._enh_matrix[:] = value
        else:
            raise IllegalAssignmentError('enh_matrix')

    @property
    def objmask(self) -> ObjectMask:
        """Returns the ObjectMask Accessor; The object mask is a mutable binary representation of the objects in an image to be analyzed. Changing elements of the mask will reset object_map labeling.

        Note:
            - If the image has not been processed by a detector, the target for analysis is the entire image itself. Accessing the object_mask in this case
                will return a 2-D array entirely with value 1 that is the same shape as the matrix
            - Changing elements of the mask will relabel of objects in the object_map (A workaround to this issue may or may not come in future versions)

        Returns:
            ObjectMaskErrors: A mutable binary representation of the objects in an image to be analyzed.

        See Also: :class:`ObjectMask`
        """
        if self._sparse_object_map is None:
            raise EmptyImageError
        else:
            return self.__object_mask_subhandler

    @objmask.setter
    def objmask(self, object_mask):
        if isinstance(object_mask, np.ndarray):
            self.objmask[:] = object_mask
        else:
            raise IllegalAssignmentError('object_mask')

    @property
    def objmap(self) -> ObjectMap:
        """Returns the ObjectMap accessor; The object map is a mutable integer matrix that identifies the different objects in an image to be analyzed. Changes to elements of the object_map sync to the object_mask.

        The object_map is stored as a compressed sparse column matrix in the backend. This is to save on memory consumption at the cost of adding
        increased computational overhead between converting between sparse and dense matrices.

        Note:
            - Has accessor methods to get sparse representations of the object map that can streamline measurement calculations.

        Returns:
            ObjectMap: A mutable integer matrix that identifies the different objects in an image to be analyzed.

        See Also: :class:`ObjectMap`
        """
        if self._sparse_object_map is None:
            raise EmptyImageError
        else:
            return self.__object_map_subhandler

    @objmap.setter
    def objmap(self, object_map):
        if isinstance(object_map, np.ndarray):
            self.objmap[:] = object_map
        else:
            raise IllegalAssignmentError('object_map')

    @property
    def props(self) -> list[ski.measure._regionprops.RegionProperties]:
        """Fetches the properties of labeled regions in an image.

        Calculates region properties for the entire image using the matrix representation.
        The labeled image is generated as a full array with values of 1, and the
        intensity image corresponds to the `_matrix` attribute of the object.
        Cache is disabled in this configuration.

        Returns:
            list[skimage.measure._regionprops.RegionProperties]: A list of properties for the entire provided image.

        Notes:
            (Excerpt from skimage.measure.regionprops documentation on available properties.):

            Read more at :class:`skimage.measure.regionprops`

            area: float
                Area of the region i.e. number of pixels of the region scaled by pixel-area.

            area_bbox: float
                Area of the bounding box i.e. number of pixels of bounding box scaled by pixel-area.

            area_convex: float
                Area of the convex hull image, which is the smallest convex polygon that encloses the region.

            area_filled: float
                Area of the region with all the holes filled in.

            axis_major_length: float
                The length of the major axis of the ellipse that has the same normalized second central moments as the region.

            axis_minor_length: float
                The length of the minor axis of the ellipse that has the same normalized second central moments as the region.

            bbox: tuple
                Bounding box (min_row, min_col, max_row, max_col). Pixels belonging to the bounding box are in the half-open interval [min_row; max_row) and [min_col; max_col).

            centroid: array
                Centroid coordinate tuple (row, col).

            centroid_local: array
                Centroid coordinate tuple (row, col), relative to region bounding box.

            centroid_weighted: array
                Centroid coordinate tuple (row, col) weighted with intensity image.

            centroid_weighted_local: array
                Centroid coordinate tuple (row, col), relative to region bounding box, weighted with intensity image.

            coords_scaled(K, 2): ndarray
                Coordinate list (row, col) of the region scaled by spacing.

            coords(K, 2): ndarray
                Coordinate list (row, col) of the region.

            eccentricity: float
                Eccentricity of the ellipse that has the same second-moments as the region. The eccentricity is the ratio of the focal distance (distance between focal points) over the major axis length. The value is in the interval [0, 1). When it is 0, the ellipse becomes a circle.

            equivalent_diameter_area: float
                The diameter of a circle with the same area as the region.

            euler_number: int
                Euler characteristic of the set of non-zero pixels. Computed as number of connected components subtracted by number of holes (input.ndim connectivity). In 3D, number of connected components plus number of holes subtracted by number of tunnels.

            extent: float
                Ratio of pixels in the region to pixels in the total bounding box. Computed as area / (rows * cols)

            feret_diameter_max: float
                Maximum Feret’s diameter computed as the longest distance between points around a region’s convex hull contour as determined by find_contours. [5]

            image(H, J): ndarray
                Sliced binary region image which has the same size as bounding box.

            image_convex(H, J): ndarray
                Binary convex hull image which has the same size as bounding box.

            image_filled(H, J): ndarray
                Binary region image with filled holes which has the same size as bounding box.

            image_intensity: ndarray
                Image inside region bounding box.

            inertia_tensor: ndarray
                Inertia tensor of the region for the rotation around its mass.

            inertia_tensor_eigvals: tuple
                The eigenvalues of the inertia tensor in decreasing order.

            intensity_max: float
                Value with the greatest intensity in the region.

            intensity_mean: float
                Value with the mean intensity in the region.

            intensity_min: float
                Value with the least intensity in the region.

            intensity_std: float
                Standard deviation of the intensity in the region.

            label: int
                The label in the labeled input image.

            moments(3, 3): ndarray
                Spatial moments up to 3rd order::

                    m_ij = sum{ array(row, col) * row^i * col^j }

            where the sum is over the row, col coordinates of the region.

            moments_central(3, 3): ndarray
                Central moments (translation invariant) up to 3rd order::

                    mu_ij = sum{ array(row, col) * (row - row_c)^i * (col - col_c)^j }

                where the sum is over the row, col coordinates of the region, and row_c and col_c are the coordinates of the region’s centroid.

            moments_hu: tuple
                Hu moments (translation, scale and rotation invariant).

            moments_normalized(3, 3): ndarray
                Normalized moments (translation and scale invariant) up to 3rd order::

                    nu_ij = mu_ij / m_00^[(i+j)/2 + 1]

                where m_00 is the zeroth spatial moment.

            moments_weighted(3, 3): ndarray
                Spatial moments of intensity image up to 3rd order::

                    wm_ij = sum{ array(row, col) * row^i * col^j }

                where the sum is over the row, col coordinates of the region.

            moments_weighted_central(3, 3): ndarray
                Central moments (translation invariant) of intensity image up to 3rd order::

                    wmu_ij = sum{ array(row, col) * (row - row_c)^i * (col - col_c)^j }

                where the sum is over the row, col coordinates of the region, and row_c and col_c are the coordinates of the region’s weighted centroid.

            moments_weighted_hu: tuple
                Hu moments (translation, scale and rotation invariant) of intensity image.

            moments_weighted_normalized(3, 3): ndarray
                Normalized moments (translation and scale invariant) of intensity image up to 3rd order::

                    wnu_ij = wmu_ij / wm_00^[(i+j)/2 + 1]

                where wm_00 is the zeroth spatial moment (intensity-weighted area).

            num_pixels: int
                Number of foreground pixels.

            orientation: float
                Angle between the 0th axis (rows) and the major axis of the ellipse that has the same second moments as the region, ranging from -pi/2 to pi/2 counter-clockwise.

            perimeter: float
                Perimeter of object which approximates the contour as a line through the centers of border pixels using a 4-connectivity.

            perimeter_crofton: float
                Perimeter of object approximated by the Crofton formula in 4 directions.

            slice: tuple of slices
                A slice to extract the object from the source image.

            solidity: float
                Ratio of pixels in the region to pixels of the convex hull image.

        References:
            https://scikit-image.org/docs/stable/api/skimage.measure.html#skimage.measure.regionprops


        """
        return ski.measure.regionprops(label_image=np.full(shape=self.shape, fill_value=1), intensity_image=self._matrix, cache=False)

    @property
    def objects(self) -> ImageObjects:
        """Returns an acessor to the objects in an image and perform operations on them, such as measurement calculations.

        This method provides access to `ImageObjects`.

        Returns:
            ImageObjects: The subhandler instance that manages image-related objects.

        Raises:
            NoObjectsError: If no objects are targeted in the image. Apply an ObjectDetector first.
        """
        if self.num_objects == 0:
            raise NoObjectsError(self.name)
        else:
            return self.__objects_subhandler

    @objects.setter
    def objects(self, objects):
        raise IllegalAssignmentError('objects')

    @property
    def num_objects(self) -> int:
        """Returns the number of objects in the image
        Note:
            If the number of objects is 0, the target for analysis is the entire image itself.
        """
        object_labels = np.unique(self._sparse_object_map.data)
        return len(object_labels[object_labels != 0])

    def copy(self):
        """Creates a copy of the current Image instance, excluding the UUID.
        Note:
            - The new instance is only informationally a copy. The UUID of the new instance is different.

        Returns:
            Image: A copy of the current Image instance.
        """
        # Create a new instance of ImageHandler
        return self.__class__(self)

    def imread(self, filepath: PathLike) -> Type[Image]:
        """
        Reads an image file from a given file path, processes it as per its format, and sets the image
        along with its schema in the current instance. Supports RGB formats (png, jpg, jpeg) and
        grayscale formats (tif, tiff). The name of the image processing instance is updated to match
        the file name without the extension. If the file format is unsupported, an exception is raised.

        Args:
            filepath (PathLike): Path to the image file to be read.

        Returns:
            Type[Image]: The current instance with the newly loaded image and schema.

        Raises:
            UnsupportedFileType: If the file format is not supported.
        """
        # Convert to Path object
        filepath = Path(filepath)
        if filepath.suffix in ['.png', '.jpg', '.jpeg']:
            self.set_image(
                input_image=ski.io.imread(filepath), imformat=IMAGE_FORMATS.RGB
            )
            self.name = filepath.stem
            return self
        elif filepath.suffix in ['.tif', '.tiff']:
            self.set_image(
                input_image=ski.io.imread(filepath), imformat=IMAGE_FORMATS.GRAYSCALE
            )
            self.name = filepath.stem
            return self
        else:
            raise UnsupportedFileTypeError(filepath.suffix)

    def set_image(self, input_image: Image | np.ndarray, imformat: str = None) -> None:
        """Sets the image to the inputted array or Image

        Args:
            input_image: (np.ndarray, PhenoTypic.Image) The image data to be set
            imformat: (str, optional) If input image is a np.ndarray and format is None, the image format will be guessed.
                If the image format is ambiguous between RGB/BGR it will assume RGB unless otherwise specified.
                Accepted formats are ['RGB', 'RGBA','Grayscale','BGR','BGRA','HSV']
        """
        if type(input_image) == np.ndarray:
            self._set_from_array(input_image, imformat)
        elif (type(input_image) == self.__class__
              or isinstance(input_image, self.__class__)
              or issubclass(type(input_image), ImageHandler)):
            self._set_from_class_instance(input_image)
        elif input_image is None:
            self.__image_format = None
            self._array = None
            self._matrix = None
            self._enh_matrix = None
            self._sparse_object_map = None

    def _set_from_class_instance(self, class_instance):
        self.__image_format = class_instance.imformat

        if class_instance.imformat not in IMAGE_FORMATS.MATRIX_FORMATS:
            self._set_from_array(class_instance.array[:].copy(), class_instance.imformat)
        else:
            self._set_from_array(class_instance.matrix[:].copy(), class_instance.imformat)
        self._enh_matrix = class_instance._enh_matrix.copy()
        self._sparse_object_map = class_instance._sparse_object_map.copy()
        self._protected_metadata = deepcopy(class_instance._protected_metadata)
        self._public_metadata = deepcopy(class_instance._public_metadata)

    def _set_from_matrix(self, matrix: np.ndarray):
        """Initializes all the 2-D components of an image

        Args:
            matrix: A 2-D array form of an image
        """
        self._matrix = matrix.copy()
        self.__enh_matrix_accessor.reset()

        if self._sparse_object_map is None or matrix.shape != self._sparse_object_map.shape:
            self.__object_map_subhandler.reset()

    def _set_from_rgb(self, rgb_array: np.ndarray):
        """Initializes all the components of an image from an RGB array

        """
        self._array = rgb_array.copy()
        self._set_from_matrix(rgb2gray(self._array.copy()))

    def _set_from_array(self, imarr: np.ndarray, imformat: str) -> None:
        """Initializes all the components of an image from an array

        Note:
            The format of the input should already have been set or guessed
        Args:
            imarr: the input image array
            imformat: (str, optional) The format of the input image
        """

        # In the event of None for schema, PhenoTypic guesses the format
        if imformat is None:
            imformat = self._guess_image_format(imarr)
            if imformat in IMAGE_FORMATS.AMBIGUOUS_FORMATS:
                # PhenoTypic will assume in the event of rgb vs bgr that the input was rgb
                self.__image_format = IMAGE_FORMATS.RGB

        match imformat:
            case 'Grayscale' | IMAGE_FORMATS.GRAYSCALE | IMAGE_FORMATS.GRAYSCALE_SINGLE_CHANNEL:
                self.__image_format = IMAGE_FORMATS.GRAYSCALE
                self._set_from_matrix(
                    imarr if imarr.ndim == 2 else imarr[:, :, 0]
                )

            case 'RGB' | IMAGE_FORMATS.RGB | IMAGE_FORMATS.RGB_OR_BGR:
                self.__image_format = IMAGE_FORMATS.RGB
                self._set_from_rgb(imarr)

            case 'RGBA' | IMAGE_FORMATS.RGBA | IMAGE_FORMATS.RGBA_OR_BGRA:
                self.__image_format = IMAGE_FORMATS.RGB
                self._set_from_rgb(rgba2rgb(imarr))

            case 'BGR' | IMAGE_FORMATS.BGR:
                self.__image_format = IMAGE_FORMATS.RGB
                warnings.warn('BGR Images are automatically converted to RGB')
                self._set_from_rgb(imarr[:, :, ::-1])

            case 'BGRA' | IMAGE_FORMATS.BGRA:
                self.__image_format = IMAGE_FORMATS.RGB
                warnings.warn('BGRA Images are automatically converted to RGB')
                self._set_from_rgb(imarr[:, :, [2, 1, 0, 3]])

            case _:
                raise ValueError(f'Unsupported image format: {imformat}')

    @staticmethod
    def _guess_image_format(img: np.ndarray) -> IMAGE_FORMATS:
        """
        Attempts to determine the color format of an image represented as a NumPy array.

        The function examines:
          - The number of dimensions (ndim) and channels (shape)
          - Basic statistics (min, max) for each channel in a 3-channel image

        Returns a string that describes the likely image format.

        Args:
            img (np.ndarray): The input image as a NumPy array.

        Returns:
            str: A string describing the guessed image format.

        Notes:
            - A 2D array is assumed to be a grayscale image.
            - A 3D array with one channel (shape: (H, W, 1)) is also treated as grayscale.
            - A 3-channel image (shape: (H, W, 3)) may be RGB, BGR, or even HSV.
              The heuristic here checks if the first channel’s maximum is within the typical
              range for Hue in an HSV image (0–179 for OpenCV) while one of the other channels
              exceeds that range.
            - A 4-channel image is assumed to be some variant of RGBA (or BGRA), but the ordering
              remains ambiguous without further metadata.
            - In many cases (especially when values are normalized or images have been post-processed),
              these heuristics may not be conclusive.
        """
        # Ensure input is a numpy array
        if not isinstance(img, np.ndarray):
            raise TypeError("Input must be a numpy array.")

        # Handle grayscale images: 2D arrays or 3D with a single channel.
        if img.ndim == 2:
            return IMAGE_FORMATS.GRAYSCALE
        if img.ndim == 3:
            h, w, c = img.shape
            if c == 1:
                return IMAGE_FORMATS.GRAYSCALE_SINGLE_CHANNEL

            # If there are 3 channels, we need to differentiate between several possibilities.
            if c == 3:
                # Compute basic statistics for each channel.
                # (These are used in heuristics; formulas: ch_i_min = min(img[..., i]),
                # ch_i_max = max(img[..., i]) for i in {0,1,2})
                ch0_min, ch0_max = np.min(img[..., 0]), np.max(img[..., 0])
                ch1_min, ch1_max = np.min(img[..., 1]), np.max(img[..., 1])
                ch2_min, ch2_max = np.min(img[..., 2]), np.max(img[..., 2])

                # Heuristic for detecting an HSV image (using OpenCV’s convention):
                # In an 8-bit image, Hue is in the range [0, 179] while Saturation and Value are in [0, 255].
                # Here, if channel 0 (possible Hue) never exceeds 180 but at least one of the other channels does,
                # it might be an HSV image.
                if ch0_max <= 180 and (ch1_max > 180 or ch2_max > 180):
                    return IMAGE_FORMATS.HSV

                # Without further metadata, we cannot distinguish between RGB and BGR.
                # Both are 3-channel images with similar ranges. This is left as ambiguous.
                return IMAGE_FORMATS.RGB_OR_BGR

            # Handle 4-channel images.
            if c == 4:
                # In many cases a 4-channel image is either RGBA or BGRA.
                # Without further context, we report it as ambiguous.
                return IMAGE_FORMATS.RGBA_OR_BGRA

            # For any other number of channels, we note it as an unknown format.
            raise ValueError(f"Image with {c} channels (unknown format)")

        # If the array has more than 3 dimensions, we don't have a standard interpretation.
        raise ValueError("Unknown format (unsupported number of dimensions)")

    def show(self,
             ax: plt.Axes = None,
             figsize: Tuple[int, int] = (9, 10)
             ) -> (plt.Figure, plt.Axes):
        """Returns a matplotlib figure and axes showing the input image"""
        if self.imformat not in IMAGE_FORMATS.MATRIX_FORMATS:
            return self.array.show(ax=ax, figsize=figsize)
        else:
            return self.matrix.show(ax=ax, figsize=figsize)

    def show_overlay(self, object_label: Optional[int] = None, ax: plt.Axes = None,
                     figsize: Tuple[int, int] = (10, 5),
                     annotate: bool = False,
                     annotation_size: int = 12,
                     annotation_color: str = 'white',
                     annotation_facecolor: str = 'red',
                     ) -> (plt.Figure, plt.Axes):
        """
        Displays an overlay of the object specified by the given label on an image or
        matrix with optional annotations.

        This method checks the schema of the object to determine whether it belongs to
        matrix formats or image formats, and delegates the overlay rendering to the
        appropriate method accordingly. It optionally allows annotations to be added
        for the specified object label with customizable style settings.

        Args:
            object_label (Optional[int]): The label of the object to overlay. If None,
                the entire image or matrix is displayed without a specific object
                highlighted.
            ax (Optional[plt.Axes]): The matplotlib Axes instance to render the overlay
                on. If None, a new figure and axes are created for rendering.
            figsize (Tuple[int, int]): Tuple specifying the size (width, height) of the
                figure to create if no axes are provided.
            annotate (bool): Whether to annotate the image/matrix using the given
                annotation settings.
            annotation_size (int): The font size of the annotations, applicable only
                when `annotate` is True.
            annotation_color (str): The color of the text annotations, applicable only
                when `annotate` is True.
            annotation_facecolor (str): The color of the annotation marker background,
                applicable only when `annotate` is True.

        Returns:
            Tuple[plt.Figure, plt.Axes]: A tuple containing the matplotlib Figure and
            Axes objects used to render the overlay.

        """
        if self.imformat not in IMAGE_FORMATS.MATRIX_FORMATS:
            return self.array.show_overlay(object_label=object_label, ax=ax, figsize=figsize,
                                           annotate=annotate, annotation_size=annotation_size,
                                           annotation_color=annotation_color, annotation_facecolor=annotation_facecolor
                                           )
        else:
            return self.matrix.show_overlay(object_label=object_label, ax=ax, figsize=figsize,
                                            annotate=annotate, annotation_size=annotation_size,
                                            annotation_color=annotation_color, annotation_facecolor=annotation_facecolor
                                            )

    def rotate(self, angle_of_rotation: int, mode: str = 'edge', **kwargs) -> None:
        """Rotate the image and all its components"""
        if self.imformat not in IMAGE_FORMATS.MATRIX_FORMATS:
            self._array = skimage_rotate(image=self._array, angle=angle_of_rotation, mode=mode, clip=True, **kwargs)

        self._matrix = skimage_rotate(image=self._matrix, angle=angle_of_rotation, mode=mode, clip=True, **kwargs)
        self._enh_matrix = skimage_rotate(image=self._enh_matrix, angle=angle_of_rotation, mode=mode, clip=True, **kwargs)

        # Rotate the object map while preserving the details and using nearest-neighbor interpolation
        self.objmap[:] = scipy_rotate(input=self.objmap[:], angle=angle_of_rotation, mode='constant', cval=0, order=0, reshape=False)

    def reset(self) -> Type[Image]:
        """
        Resets the internal state of the object and returns an updated instance.

        This method resets the state of DetectionMatrix and ObjectMap components maintained
        by the object. It ensures that the object is reset to its original state
        while maintaining its type integrity. Upon execution, the instance of the
        calling object itself is returned.

        Returns:
            Type[Image]: The instance of the object after resetting its internal
            state.
        """
        self.enh_matrix.reset()
        self.objmap.reset()
        return self
