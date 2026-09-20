import argparse
import cv2
import numpy as np

detector = cv2.QRCodeDetector()


def annotate(frame):
    text, points, _ = detector.detectAndDecode(frame)
    if points is not None:
        cv2.polylines(frame, [points.astype(np.int32)], True, (0, 255, 0), 3)
        if text:
            x, y = points[0][0].astype(int)
            cv2.putText(frame, text, (x, max(20, y - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    return frame, text


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--image")
    args = p.parse_args()
    if args.image:
        img = cv2.imread(args.image)
        if img is None:
            raise SystemExit(f"Could not read {args.image}")
        img, text = annotate(img)
        print("Decoded:", text or "(nothing found)")
        cv2.imshow("QR Scanner", img)
        cv2.waitKey(0)
    else:
        cap, last = cv2.VideoCapture(0), ""
        while cap.isOpened():
            ok, frame = cap.read()
            if not ok:
                break
            frame, text = annotate(frame)
            if text and text != last:
                print("Decoded:", text)
                last = text
            cv2.imshow("QR Scanner", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
