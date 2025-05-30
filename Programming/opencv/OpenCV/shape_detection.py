import numpy as np
import cv2
import random

# Reading the noisy image
img = cv2.imread("fuzzy.png", 1)

# Resize image to 1280x720
img = cv2.resize(img, (1280, 720))

# Display original image
cv2.imshow("Original", img)

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#POINT 2
# Apply Gaussian Blur
blur = cv2.GaussianBlur(gray, (9 , 9), 1.5)

#Point1
# Apply adaptive thresholding (binary inverse)
thresh = cv2.adaptiveThreshold(blur, 255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 205, 1)

cv2.imshow("Binary", thresh)

# Find contours
contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

print(f"Total contours: {len(contours)}")

#Point 3
# Filtered contours by area
filtered = [c for c in contours if cv2.contourArea(c) >= 3000]
print(f"Filtered contours: {len(filtered)}")

# Image to draw contours and shapes
objects = np.zeros_like(img)

# Loop over each filtered contour
for contour in filtered:
    # Random color for contour
    color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))

    # Approximate shape
    approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)

    # Draw filled contour
    cv2.drawContours(objects, [contour], -1, color, -1)

    # Compute bounding box
    x, y, w, h = cv2.boundingRect(approx)
    cv2.rectangle(objects, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Determine shape type
    shape = "Circle"
    if len(approx) == 3:
        shape = "Triangle"
    elif len(approx) == 4:
        aspect_ratio = w / float(h)
        if 0.95 <= aspect_ratio <= 1.05:
            shape = "Square"
        else:
            shape = "Rectangle"
    elif len(approx) == 5:
        shape = "Pentagon"
    elif len(approx) == 6:
        shape = "Hexagon"

    # Calculate center for placing text
    M = cv2.moments(contour)
    if M['m00'] != 0.0:
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
    else:
        cx, cy = x + w // 2, y + h // 2

    # Put shape name
    cv2.putText(objects, shape, (cx - 30, cy),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # Print area and perimeter
    area = cv2.contourArea(contour)
    perimeter = cv2.arcLength(contour, True)
    print(f"{shape}: Area = {area:.2f}, Perimeter = {perimeter:.2f}")

# Show result with labeled shapes and bounding boxes
cv2.imshow("Contours and Shapes", objects)

# Wait and close
cv2.waitKey(0)
cv2.destroyAllWindows()
