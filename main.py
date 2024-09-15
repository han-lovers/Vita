from vision_ine import vision_ine  # Assuming the class is defined in a file named vision_ine.py

a = vision_ine()
print("0%")

a.load_data('cropped_id_front.jpeg')
# a.load_back('cropped_id_back.jpeg')

print("25%")

a.load_data('cropped_id_front2.png')
# a.load_back('cropped_id_back2.jpeg')

print("50%")

a.load_data('cropped_id_front3.jpeg')
# a.load_back('cropped_id_back3.jpeg')

print("75%")

a.load_data('cropped_id_front4.jpeg')
# a.load_back('cropped_id_back4.jpeg')

print("100%")


a.save_data()