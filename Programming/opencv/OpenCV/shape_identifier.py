import cv2
import numpy as np

# Reading the image
img = cv2.imread('fuzzy.png')
img = cv2.resize(img, (1280, 720))
# Converting image into grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow("Gray",gray)
# Convert BGR to HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
cv2.imshow("hsv",hsv)
# Define HSV range for blue (adjust as needed)
lower_blue = np.array([80, 140, 50])
upper_blue = np.array([100, 255, 255])

# Threshold the HSV image to get only blue colors
mask = cv2.inRange(hsv, lower_blue, upper_blue)

# Bitwise-AND mask and original image
result = cv2.bitwise_and(img, img, mask=mask)

cv2.imshow('Mask (Blue regions)', mask)
cv2.imshow('Filtered Image', result)

# Thresholding the grayscale image
_, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
cv2.imshow("threshold",threshold)

# Finding contours
contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


i = 0

# Looping through contours
for contour in contours:
    # Skip the first contour (the outer frame)
    if i == 0:
        i = 1
        continue

    # Approximating the shape
    approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)

    # Drawing the contour
    cv2.drawContours(img, [contour], 0, (0, 0, 255), 2)

    # Calculating center
    M = cv2.moments(contour)
    if M['m00'] != 0.0:
        x = int(M['m10'] / M['m00'])
        y = int(M['m01'] / M['m00'])

    # Finding bounding box
    x_box, y_box, w_box, h_box = cv2.boundingRect(approx)
    cv2.rectangle(img, (x_box, y_box), (x_box + w_box, y_box + h_box), (0, 255, 0), 2)

    # Determining shape
    shape_name = "Circle"
    if len(approx) == 3:
        shape_name = "Triangle"
    elif len(approx) == 4:
        # Check for square or rectangle
        aspect_ratio = w_box / float(h_box)
        if 0.95 <= aspect_ratio <= 1.05:
            shape_name = "Square"
        else:
            shape_name = "Rectangle"
    elif len(approx) == 5:
        shape_name = "Pentagon"
    elif len(approx) == 6:
        shape_name = "Hexagon"

    # Displaying shape name inside the bounding box
    cv2.putText(img, shape_name, (x_box + 5, y_box + 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

# Display the final image
cv2.imshow('Detected Shapes with Bounding Boxes', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
