# OCR Tester

## Description
This is the final project in Software Testing course. In this project, we were asked to test an OCR (optical character recognition) engine 
called Tesseract, which is an open-source program.
The main part of the project was to write a test strategy for the program, and to implement 
it in python.
As you can imagine, the number of tests that can be executed is infinite, so the real challenge 
was to generate enough tests which will make our automation program to be sound, efficient 
and effective.

## Tesseract Testing Specification
We were asked to test Tesseract under the following specifications:
1. The supported fonts are the ones listed in "fonts" directory. 
2. Supported languages: English, Hebrew, Swedish, Spanish. 
3. Supported font sizes: All font sizes between 8 and 72. 
4. The text can be anywhere in the image, without limitations, as long as the full characters 
are in the image and are not overlapping other characters. There is no guarantee on 
results for characters that are partially in the image (truncated characters) or overlapped. 
5. The text in the image can have any number of lines and the lines can be of any length 
(number of characters). Any length of text is supported. 
6. The OCR is not supported on “text in the wild” (text from pictures taken from real-life, 
e.g. street signs). The text for OCR should be text from a text editors, using the 
supported fonts. 
7. The OCR is limited to text angled at 0°, 90°, 180° and 270° degrees rotation (0° means 
horizontal text with no rotation). 
8. The OCR supports only black text on white background (i.e. don’t test with colors – bugs 
involving colors won’t be accepted for this exercise).
9. Configuration parameters of Tesseract: 
    tessedit_char_blacklist 
    tessedit_char_unblacklist 
    tessedit_char_whitelist 
    page_separator 
    tessedit_load_sublangs

## Our implementation
###### Text2Image.py
Firstly, we generated about 232 images in which we will use to test Tesseract.
We made a short program that recieves a text, font, font size, position, img format and image dimensions,
and generates an image with the rellevant credentials. 

###### Additional Files/input_artium.csv
According to our test strategy, and using the generated images, we created a total of 336 tests 
listed in this csv file. Each row in the table represents a test, which consists of:
1. The tested image. 
2. The expected output from Tesseract. 
3. The configuration parameters given to Tesseract.

###### project_artium.py
In this file we implemented our test automation program. 
For each row (test) from input_artium.csv, the program:
1. Parse the test details.
2. Run tesseract on the given image.
3. Compares Tesseract output to the expected output.

###### testResults_artuim.csv
Finally, we stored the test results in this file. 

## Software Testing Course
Software Testing is an elective course in computer science bachelor's program.
The course staff are software testers from Intel, and as part of the course content, 
we learned all kind of topics related to testing:
* Exploratory testing. 
* Test desing techniques as boundary values, equivalence classes etc.
* Test automation.
* Bug reporting.
... and more.
