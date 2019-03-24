#!/usr/bin/env python
# coding: utf-8
import yaml
import numpy as np
import cv2

def getFrame(cite):

    resource = cite
    resource_name = resource
    print("Trying to open resource: " + resource_name)
    cap = cv2.VideoCapture(resource)
    if not cap.isOpened():
        print("Error opening resource: " + str(resource))
        print("Maybe opencv VideoCapture can't open it")
        exit(0)
    print("Correctly opened resource, starting to show feed.")
    rval, frame = cap.read()
    return frame


# In[5]:
def parkingDataProcessing(cite:String = "http://flussonic-12.cams.ufanet.ru/1492065333/preview.mp4?token=bdee398372054f46ae1949cc299df92a", day:bool = true):
    fn_yaml = "Khare_yml_02.yml"
    fn_out =  "output.mp4"
    cascade_src = 'Khare_classifier_02.xml'
    car_cascade = cv2.CascadeClassifier(cascade_src)
    global_str = "Последнее изменение на: "
    change_pos = 0.00
    dict =  {
            'text_overlay': True,
            'parking_overlay': True,
            'parking_id_overlay': True,
            'parking_detection': True,
            'motion_detection': True,
            'pedestrian_detection': False, # занимает много вычислительной мощности
            'min_area_motion_contour': 500, # область, заданная для обнаружения движения
            'park_laplacian_th': 4.14,
            'park_sec_to_wait': 1, # 4   время ожидания изменения статуса области
            'start_frame': 0, # начать кадр с определенного номера кадра
            'show_ids': True, # показывает id в каждой области
            'classifier_used': True,
            'save_video': False
            }

    if not day:
        dict['park_laplacian_th'] = 2.0
    # Сбор видео из потока

    imgs = [getFrame(cite) for i in range(80)]
    height, width, layers = imgs[0].shape
    print(height, width, layers)

    writer = cv2.VideoWriter(
        fn_out,
        cv2.VideoWriter_fourcc(*'MJPG'),   # codec
        25.0,  # fps
        (width, height),  # width, height
        isColor=len(imgs[0].shape) > 2)

    for frame in imgs:
        writer.write(frame)

    writer.release()
    cap = cv2.VideoCapture('output.mp4')
    video_info = {  'fps':    cap.get(cv2.CAP_PROP_FPS),
                    'width':  int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)*0.6),
                    'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)*0.6),
                    'fourcc': cap.get(cv2.CAP_PROP_FOURCC),
                    'num_of_frames': int(cap.get(cv2.CAP_PROP_FRAME_COUNT))}

    cap.set(cv2.CAP_PROP_POS_FRAMES, dict['start_frame']) # перейти к указанному номеру кадра

    def run_classifier(img, id):
        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cars = car_cascade.detectMultiScale(img, 1.1, 1)
        if cars == ():
            return False
        else:
            # parking_status[id] = False
            return True

    # Определить кодек и создать объект VideoWriter
    if dict['save_video']:
        fourcc = cv2.VideoWriter_fourcc('X','V','I','D') # options: ('P','I','M','1'), ('D','I','V','X'), ('M','J','P','G'), ('X','V','I','D')
        out = cv2.VideoWriter(fn_out, -1, 25.0,(video_info['width'], video_info['height']))

    # Инициализирует детектор дескриптора HOG / человека. Занимает много вычислительной мощности.
    if dict['pedestrian_detection']:
        hog = cv2.HOGDescriptor()
        hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

        # Использовать вычитание фона
    if dict['motion_detection']:
        fgbg = cv2.createBackgroundSubtractorMOG2(history=300, varThreshold=16, detectShadows=True)

    # Чтение данных YAML (полигоны парковочных мест)
    with open(fn_yaml, 'r') as stream:
        parking_data = yaml.load(stream)
    parking_contours = []
    parking_bounding_rects = []
    parking_mask = []
    parking_data_motion = []
    if parking_data != None:
        for park in parking_data:
            points = np.array(park['points'])
            rect = cv2.boundingRect(points)
            points_shifted = points.copy()
            points_shifted[:,0] = points[:,0] - rect[0] # смещение контура в область интереса
            points_shifted[:,1] = points[:,1] - rect[1]
            parking_contours.append(points)
            parking_bounding_rects.append(rect)
            mask = cv2.drawContours(np.zeros((rect[3], rect[2]), dtype=np.uint8), [points_shifted], contourIdx=-1,
                                        color=255, thickness=-1, lineType=cv2.LINE_8)
            mask = mask==255
            parking_mask.append(mask)

    kernel_erode = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3)) # morphological kernel
    kernel_dilate = cv2.getStructuringElement(cv2.MORPH_RECT,(5,19))
    if parking_data != None:
        parking_status = [False]*len(parking_data)
        parking_buffer = [None]*len(parking_data)
    # bw = ()
    def print_parkIDs(park, coor_points, frame_rev):
        moments = cv2.moments(coor_points)
        centroid = (int(moments['m10']/moments['m00'])-3, int(moments['m01']/moments['m00'])+3)
        # нанесение номеров на отмеченные области
        cv2.putText(frame_rev, str(park['id']), (centroid[0]+1, centroid[1]+1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
        cv2.putText(frame_rev, str(park['id']), (centroid[0]-1, centroid[1]-1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
        cv2.putText(frame_rev, str(park['id']), (centroid[0]+1, centroid[1]-1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
        cv2.putText(frame_rev, str(park['id']), (centroid[0]-1, centroid[1]+1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
        cv2.putText(frame_rev, str(park['id']), centroid, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)


    while(cap.isOpened()):
        video_cur_pos = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0 # Текущее положение видеофайла в секундах
        video_cur_frame = cap.get(cv2.CAP_PROP_POS_FRAMES) # Индекс кадра, который будет декодирован / захвачен далее
        ret, frame_initial = cap.read()
        if ret == True:
            frame = cv2.resize(frame_initial, None, fx=0.6, fy=0.6)
        if ret == False:
            print("Video ended")
            break

        # Вычитание фона
        frame_blur = cv2.GaussianBlur(frame.copy(), (5,5), 3)
        # frame_blur = frame_blur[150:1000, 100:1800]
        frame_gray = cv2.cvtColor(frame_blur, cv2.COLOR_BGR2GRAY)
        frame_out = frame.copy()


        # обнаружение автомобилей и свободных мест
        if dict['parking_detection']:
            for ind, park in enumerate(parking_data):
                points = np.array(park['points'])
                rect = parking_bounding_rects[ind]
                roi_gray = frame_gray[rect[1]:(rect[1]+rect[3]), rect[0]:(rect[0]+rect[2])] # crop roi for faster calcluation

                laplacian = cv2.Laplacian(roi_gray, cv2.CV_64F)
                # cv2.imshow('oir', laplacian)
                points[:,0] = points[:,0] - rect[0] # shift contour to roi
                points[:,1] = points[:,1] - rect[1]
                delta = np.mean(np.abs(laplacian * parking_mask[ind]))

                status = delta < dict['park_laplacian_th']
                # Если обнаружено изменение состояния парковки, сохраните текущее время
                if status != parking_status[ind] and parking_buffer[ind]==None:
                    parking_buffer[ind] = video_cur_pos
                    change_pos = video_cur_pos

                # Если состояние по-прежнему отличается от сохраненного и счетчик открыт
                elif status != parking_status[ind] and parking_buffer[ind]!=None:
                    if video_cur_pos - parking_buffer[ind] > dict['park_sec_to_wait']:
                        parking_status[ind] = status
                        parking_buffer[ind] = None
                # Если статус все тот же и счетчик открыт
                elif status == parking_status[ind] and parking_buffer[ind]!=None:
                    parking_buffer[ind] = None

        busy = 0
        free = 0
        # изменение цвета на основе изменения статуса произошло в приведенном выше разделе и нанесение чисел на области
        if dict['parking_overlay']:
            for ind, park in enumerate(parking_data):
                points = np.array(park['points'])
                if parking_status[ind]:
                    color = (0,255,0)

                    rect = parking_bounding_rects[ind]
                    roi_gray_ov = frame_gray[rect[1]:(rect[1] + rect[3]),
                                   rect[0]:(rect[0] + rect[2])]  # crop roi для более быстрого вычисления
                    res = run_classifier(roi_gray_ov, ind)
                    if res:
                        parking_data_motion.append(parking_data[ind])
                        # del parking_data[ind]
                        color = (0,0,255)
                        busy = busy + 1
                    free = free + 1
                else:
                    color = (0,0,255)
                    busy = busy + 1

                cv2.drawContours(frame_out, [points], contourIdx=-1,
                                     color=color, thickness=2, lineType=cv2.LINE_8)
                if dict['show_ids']:
                        print_parkIDs(park, points, frame_out)


        # Рисование наложения. Наложение текста в левом углу экрана
        if dict['text_overlay']:
            str_on_frame = "%d/%d" % (video_cur_frame, video_info['num_of_frames'])
#             cv2.putText(frame_out, str_on_frame, (5,30), cv2.FONT_HERSHEY_SIMPLEX,
#                             0.8, (0,255,255), 2, cv2.LINE_AA)
            cv2.putText(frame_out, str(round(change_pos,2)) + 'sec', (5, 60), cv2.FONT_HERSHEY_SIMPLEX,
                            0.8, (255, 0, 0), 2, cv2.LINE_AA)
            cv2.putText(frame_out,"Busy: " + str(busy - 1) + '.     Free: ' + str(free ), (5, 90), cv2.FONT_HERSHEY_SIMPLEX,
                            0.8, (0, 255, 0), 2, cv2.LINE_AA)


        if parking_data_motion != []:
            for index, park_coord in enumerate(parking_data_motion):
                points = np.array(park_coord['points'])
                color = (0, 0, 255)
                recta = parking_bounding_rects[ind]
                roi_gray1 = frame_gray[recta[1]:(recta[1] + recta[3]),
                                recta[0]:(recta[0] + recta[2])]  # crop roi для более быстрого вычисления

                fgbg1 = cv2.createBackgroundSubtractorMOG2(history=300, varThreshold=16, detectShadows=True)
                roi_gray1_blur = cv2.GaussianBlur(roi_gray1.copy(), (5, 5), 3)

                fgmask1 = fgbg1.apply(roi_gray1_blur)
                bw1 = np.uint8(fgmask1 == 255) * 255
                bw1 = cv2.erode(bw1, kernel_erode, iterations=1)
                bw1 = cv2.dilate(bw1, kernel_dilate, iterations=1)

                (_, cnts1, _) = cv2.findContours(bw1.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                # Цикл по контуру
                for c in cnts1:
                    print(cv2.contourArea(c))
                    # если контур слишком мал, мы его игнорируем
                    if cv2.contourArea(c) < 4:
                        continue
                    (x, y, w, h) = cv2.boundingRect(c)
                    classifier_result1 = run_classifier(roi_gray1, index)
                    if classifier_result1:
                    # print(classifier_result)
                        color = (0, 0, 255)  # Красный снова, если автомобиль найден классификатором
                    else:
                        color = (0,255, 0)
                classifier_result1 = run_classifier(roi_gray1, index)
                if classifier_result1:
                    # print(classifier_result)
                    color = (0, 0, 255)  # Красный снова, если автомобиль найден классификатором
                else:
                    color = (0, 255, 0)
                cv2.drawContours(frame_out, [points], contourIdx=-1,
                                     color=color, thickness=2, lineType=cv2.LINE_8)

        if dict['pedestrian_detection']:
            # обнаружение людей на изображении. Замедляет работу программы, требует высокой скорости ГПУ
            (rects, weights) = hog.detectMultiScale(frame, winStride=(4, 4), padding=(8, 8), scale=1.05)
            # нарисовать рамки
            for (x, y, w, h) in rects:
                cv2.rectangle(frame_out, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # писать в выходных кадрах
        if dict['save_video']:
    #         if video_cur_frame % 35 == 0: # принимать каждые 30 кадров
                out.write(frame_out)
    cv2.imwrite('frame.jpg', frame_out)
    cap.release()
    if dict['save_video']: out.release()
    cv2.destroyAllWindows()
    return  busy, free

# In[31]:

for drawingRectangles():
    # нажмите escape, чтобы закончить боксинг в реальном времени.
    # Программа отмечает полигоны на рисунке, когда получает 4 двойных клика
    import cv2
    import yaml
    import numpy as np

    refPt = []
    cropping = False
    data = []
    file_path = 'Khare_yml_02.yml'
    img = cv2.imread('parking.png')

    def yaml_loader(file_path):
        with open(file_path, "r") as file_descr:
            data = yaml.load(file_descr)
            return data


    def yaml_dump(file_path, data):
        with open(file_path, "a") as file_descr:
            yaml.dump(data, file_descr)


    def yaml_dump_write(file_path, data):
        with open(file_path, "w") as file_descr:
            yaml.dump(data, file_descr)


    def click_and_crop(event, x, y, flags, param):
        current_pt = {'id': 0, 'points': []}
        # grab references to the global variables
        global refPt, cropping
        if event == cv2.EVENT_LBUTTONDOWN:
            refPt.append((x, y))
            cropping = False
        if len(refPt) == 4:
            if data == []:
                if yaml_loader(file_path) != None:
                    data_already = len(yaml_loader(file_path))
                else:
                    data_already = 0
            else:
                if yaml_loader(file_path) != None:
                    data_already = len(data) + len(yaml_loader(file_path))
                else:
                    data_already = len(data)

            cv2.line(image, refPt[0], refPt[1], (0, 255, 0), 1)
            cv2.line(image, refPt[1], refPt[2], (0, 255, 0), 1)
            cv2.line(image, refPt[2], refPt[3], (0, 255, 0), 1)
            cv2.line(image, refPt[3], refPt[0], (0, 255, 0), 1)

            temp_lst1 = list(refPt[2])
            temp_lst2 = list(refPt[3])
            temp_lst3 = list(refPt[0])
            temp_lst4 = list(refPt[1])

            current_pt['points'] = [temp_lst1, temp_lst2, temp_lst3, temp_lst4]
            current_pt['id'] = data_already
            data.append(current_pt)
            # data_already+=1
            refPt = []
    image = cv2.resize(img, None, fx=0.6, fy=0.6)
    clone = image.copy()
    cv2.namedWindow("Double click to mark points")
    cv2.imshow("Double click to mark points", image)
    cv2.setMouseCallback("Double click to mark points", click_and_crop)

    # keep looping until the 'q' key is pressed
    while True:
        # display the image and wait for a keypress
        cv2.imshow("Double click to mark points", image)
        key = cv2.waitKey(1) & 0xFF
        if cv2.waitKey(33) == 27:
            break

    # data list into yaml file
    if data != []:
        yaml_dump(file_path, data)
    cv2.destroyAllWindows() #important to prevent window from becoming inresponsive


# In[21]:

fun showAverageAndMean():
    # Программа для демонстрации расчета порогового значения для данного парковочного устройства
    import statistics
    import cv2
    import yaml
    import numpy as np

    sum_up = 0.0
    delta_list = []
    frame = cv2.imread('Khare_frame_02.png') #
    parking_bounding_rects = []
    parking_mask = []
    frame_blur = cv2.GaussianBlur(frame.copy(), (5,5), 3)
    frame_gray = cv2.cvtColor(frame_blur, cv2.COLOR_BGR2GRAY)
    with open('Khare_yml_03.yml', 'r') as stream:
        parking_data = yaml.load(stream)

    if parking_data != None:
        for park in parking_data:
            points = np.array(park['points'])
            rect = cv2.boundingRect(points)
            points_shifted = points.copy()
            points_shifted[:,0] = points[:,0] - rect[0] # смещение контура в область интереса
            points_shifted[:,1] = points[:,1] - rect[1]

            parking_bounding_rects.append(rect)
            mask = cv2.drawContours(np.zeros((rect[3], rect[2]), dtype=np.uint8), [points_shifted], contourIdx=-1,
                                        color=255, thickness=-1, lineType=cv2.LINE_8)
            mask = mask==255
            parking_mask.append(mask)

    for ind, park in enumerate(parking_data):
            points = np.array(park['points'])
            rect = parking_bounding_rects[ind]
            roi_gray = frame_gray[rect[1]:(rect[1]+rect[3]), rect[0]:(rect[0]+rect[2])] # crop roi for faster calcluation

            laplacian = cv2.Laplacian(roi_gray, cv2.CV_64F)
            points[:,0] = points[:,0] - rect[0] # привести контур к roi
            points[:,1] = points[:,1] - rect[1]
            delta = np.mean(np.abs(laplacian * parking_mask[ind]))
            if(delta > 1.8):    # игнорирование пустых пространств
                delta_list.append(delta)
                # print(delta)
            sum_up = sum_up + delta

    avg = sum_up/len(parking_data)
    med = statistics.median(delta_list)
    print("mean: ", avg)
    print("median: ", med)
