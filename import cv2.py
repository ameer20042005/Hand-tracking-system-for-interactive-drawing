import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector

# فتح الكاميرا
video = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# ضبط أبعاد الفيديو
video.set(3, 720)  # العرض
video.set(4, 480)  # الارتفاع

# إنشاء كائن لكشف اليد
detector = HandDetector()

# قائمة لتخزين النقاط المرسومة
desenho = []

while True:
    # قراءة إطار الفيديو
    check, img = video.read()

    # قلب صورة الكاميرا أفقيًا
    img = cv2.flip(img, 1)

    # خلق قماش أبيض للرسم عليه
    canvas = np.ones_like(img) * 255

    # كشف اليد في الصورة
    resultado = detector.findHands(img, draw=True)
    hand = resultado[0]  # الحصول على معلومات اليد

    if hand:
        # الحصول على مواقع النقاط المرجعية لليد
        lmlist = hand[0]['lmList']

        # تحديد الأصابع المرفوعة
        dedos = detector.fingersUp(hand[0])
        dedosLev = dedos.count(1)  # عدد الأصابع المرفوعة

        if dedosLev == 1:
            # إذا كان الإصبع السبابة فقط مرفوعاً، نرسم دائرة صغيرة في النقطة
            x, y = lmlist[8][0], lmlist[8][1]  # موقع النقطة المرجعية للإصبع السبابة
            cv2.circle(canvas, (x, y), 15, (0, 0, 255), cv2.FILLED)
            desenho.append((x, y))  # إضافة النقطة إلى قائمة الرسم
        elif dedosLev >= 2:
            # إذا كانت الأصابع المرفوعة أكثر من واحدة، نوقف الرسم
            desenho.append((0, 0))  # إضافة نقطة توقف
            # يمكنك أيضاً مسح الرسم الحالي إذا رغبت في ذلك:
            # desenho = []

        # رسم النقاط والخطوط على القماش
        for id, ponto in enumerate(desenho):
            x, y = ponto[0], ponto[1]
            if x != 0 and y != 0:
                cv2.circle(canvas, (x, y), 10, (0, 0, 255), cv2.FILLED)

            if id >= 1:
                ax, ay = desenho[id - 1][0], desenho[id - 1][1]
                if x != 0 and ax != 0:
                    cv2.line(canvas, (x, y), (ax, ay), (0, 0, 255), 20)

    # عرض الفيديو من الكاميرا
    cv2.imshow('Camera Feed', img)

    # عرض القماش الأبيض مع الرسم
    cv2.imshow('Canvas', canvas)

    # كسر الحلقة عند الضغط على زر "Esc" أو إعادة تعيين الرسم عند الضغط على زر "Space"
    key = cv2.waitKey(1)
    if key == 27:  # زر "Esc"
        break
    elif key == 32:  # زر "Space"
        desenho = []  # إعادة تعيين الرسم

# تحرير الموارد
video.release()
cv2.destroyAllWindows()