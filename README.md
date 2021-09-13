# Auto-follow robotics system
ระบบหุ่นยนต์ติดตามเป้าหมาย 
พัฒนาด้วย openCV และ YOLOV3
## SETTING
ให้ create folder ชื่อ "datasets" ขึ้นมาก่อน
ในไฟล์ creatDatasets.py และ detect_distance_classificated.py ให้แก้ webcam = cv2.VideoCapture(0) สามารถเปลี่ยน"0" เป็น "1" หรือเลขอื่นๆตามแต่ลำดับของกล้องที่เชื่อมกับคอม
## การใช้งาน
1.run โปรแกรม creatDatasets.py แล้วใส่ชื่อคนที่จะติดตาม แล้วโปรแกรมจะเริ่มถ่ายภาพจากกล้องที่setไว้ ให้ทำการถ่ายรูปคนคนนั้นแบบ fullbody โดยจะใช้เวลาประมาณ 1 นาที เพื่อถ่ายรูปบุคคลที่จะเป็นเป้าหมายการติดตาม 250 รูป ลงในโฟลเดอร์ datasets
2.ปิดโปรแกรม creatDatasets.py แล้วมา run โปรแกรม detect_distance_classificated.py แล้วใส่ส่วนสูงคนที่ติดตามในหน่อยมิลลิเมตร จากนั้นโปรแกรมจะเปิดกล้องอีกครั้งแล้วเริ่มการ detect และวัดระยะห่างหระหว่างคนในภาพกับกล้อง
