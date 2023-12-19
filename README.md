UNI: dp3154 Name: Dahe Pan
UNI: ss6635 Name: Sheng Shen

For facial recognition, there are two methods to deploy our face recognition voting. 
The first way stores pictures of faces with the label as the file name. Put these pictures in the “Known” Folder. Make sure the unknown folder is empty. Run facial_reg.py. 
The second way stores only the face encodings. This is more like worldcoin’s orb where only the hash of the irish will be stored. To use this method. We need to first establish a library of encodings. Run add_face_encoding to each time when needed to store a face encoding. This will take a picture and turn it into face encoding then store in encoding.txt. Then run facial_rec2.py.
After pass facial recognition process, user can call voteTo function to vote.
Deployment link: https://mumbai.polygonscan.com/address/0xcaeD9b24111d8f33E4947AAD54Baef34DDBEfC41#code 