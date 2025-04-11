from image_upscaling_api import upload_image

token = "53bb7cbddc4bd622731b5341fe4d2cb3"

ret = upload_image("imgs/r1.jpg", token, use_face_enhance = False, scale = 4)
print(ret)

#exit()

ret = upload_image("imgs/r1.jpg", token, use_face_enhance = False, scale = 3)
print(ret)

ret = upload_image("imgs/r1.jpg", token, use_face_enhance = False, scale = 2)
print(ret)

ret = upload_image("imgs/r1.jpg", token, use_face_enhance = False, scale = 1)
print(ret)

ret = upload_image("imgs/r2.jpg", token, use_face_enhance = False, scale = 2)
print(ret)

ret = upload_image("imgs/r2.jpg", token, use_face_enhance = False, scale = 4)
print(ret)

ret = upload_image("imgs/r3.jpg", token, use_face_enhance = True, scale = 4)
print(ret)

ret = upload_image("imgs/r7.png", token, use_face_enhance = True, scale = 4)
print(ret)

ret = upload_image("imgs/r9.png", token, use_face_enhance = True, scale = 4)
print(ret)

ret = upload_image("imgs/r9.png", token, use_face_enhance = False, scale = 4)
print(ret)

ret = upload_image("imgs/r9.png", token, use_face_enhance = True, scale = 2)
print(ret)

ret = upload_image("imgs/r10.png", token, use_face_enhance = True, scale = 4)
print(ret)

ret = upload_image("imgs/r10.png", token, use_face_enhance = True, scale = 2)
print(ret)


from image_upscaling_api import get_uploaded_images

print(get_uploaded_images(token))