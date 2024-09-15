from vision_ine import vision_ine  # Assuming the class is defined in a file named vision_ine.py

a = vision_ine()
print("0%")

a.load_data('cropped_id_front2.jpeg')

print("25%")
#
# a.load_data('cropped_id_front.jpeg')
#
# print("50%")
#
# a.load_data('cropped_id_front3.jpeg')
#
# print("75%")
#
# a.load_data('cropped_id_front4.jpeg')
#
# print("100%")
#
# a.save_data()

a.load_back('cropped_id.jpeg')
a.join_dataframes()
a.save_data()