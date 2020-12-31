img = [1 2 3 4 5; 2 3 4 5 1; 3 4 5 1 2]
kernel1 = [1; 2; 1]
kernel2 = [-1 0 1]

kernel = kernel1 * kernel2

sobelY = conv2(img, kernel, 'valid')

step1 = img * kernel2
step2 = conv2(step1, kernel1, 'valid')
