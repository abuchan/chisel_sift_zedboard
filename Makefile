webcam_accel: webcam_accel.cpp
	g++ webcam_accel.cpp -o webcam_accel -I /usr/local/include/opencv -L /usr/local/lib -lm -lopencv_core -lopencv_highgui -lopencv_imgproc
