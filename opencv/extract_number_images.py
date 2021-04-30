import cv2


IMAGE_PATH = "../data/0.jpg"


def get_image(image_path: str = IMAGE_PATH):
    im = cv2.imread(image_path)
    return cv2.resize(im, (640, 480))


def threshold_image(image):
    frame_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    low_h = 108
    high_h = 180

    low_s = 42
    high_s = 255

    low_v = 128
    high_v = 255

    frame_threshold = cv2.inRange(frame_hsv, (low_h, low_s, low_v), (high_h, high_s, high_v))
    return frame_threshold


def find_contours(image, thresholded_image):
    contours, hierarchy = cv2.findContours(thresholded_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # filter out smaller contours
    contours = list(filter(lambda contour: cv2.contourArea(contour) > 50, contours))
    # draw_contours(contours, image)
    return contours


def draw_contours(contours, image):
    for contour in contours:
        if cv2.contourArea(contour) > 50:
            [x, y, w, h] = cv2.boundingRect(contour)

            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 255), 2)
    cv2.imshow('contours', image)
    cv2.waitKey(0)


def extract_image(image, contour):
    y = contour[1]
    y_max = y + contour[3]

    x = contour[0]
    x_max = x + contour[2]

    extract = image[y:y_max, x:x_max]
    return extract


def crop_contours(image, contours):
    images = []
    for contour in contours:
        [x, y, w, h] = cv2.boundingRect(contour)
        extracted_image = extract_image(image, [x, y, w, h])
        images.append({"bounding_rect": (x, y, w, h), "image": extracted_image})
    return images


def order_cropped_contours(contours: list):
    contours.sort(key=lambda contour: contour["bounding_rect"][0])
    return contours


def extract_ordered_numbers(image_path: str):
    image = get_image(image_path)

    # Extract numbers from image
    preprocessed_image = threshold_image(image)
    contours = find_contours(image, preprocessed_image)
    contour_crops = crop_contours(image, contours)
    order_cropped_contours(contour_crops)
    return contour_crops


def classify_extracted_image(contoured_images):
    pass


if __name__ == '__main__':
    im = get_image()

    # Extract numbers from image
    preprocessed_im = threshold_image(im)
    cnt = find_contours(im, preprocessed_im)
    cnt_im = crop_contours(im, cnt)

    # Recognize image
    cnt_numbers = classify_extracted_image(cnt_im)
