// FaceVerifyPage.jsx
// Shown when an employee's risk_score >= 90. Captures a webcam photo
// and sends it to the backend for face comparison against their
// registered profile photo.

import { useRef, useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axiosClient from "../api/axiosClient";

export default function FaceVerifyPage() {
  const { employee_id } = useParams();
  const navigate = useNavigate();
  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  const [stream, setStream] = useState(null);
  const [capturedImage, setCapturedImage] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [cameraError, setCameraError] = useState("");

  // Start the webcam when the page loads
  useEffect(() => {
    const startCamera = async () => {
      try {
        const mediaStream = await navigator.mediaDevices.getUserMedia({ video: true });
        setStream(mediaStream);
        if (videoRef.current) {
          videoRef.current.srcObject = mediaStream;
        }
      } catch (err) {
        setCameraError("Could not access webcam. Please allow camera permission and refresh.");
      }
    };
    startCamera();

    // Cleanup: stop the camera when leaving this page
    return () => {
      if (stream) {
        stream.getTracks().forEach((track) => track.stop());
      }
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const capturePhoto = () => {
    const video = videoRef.current;
    const canvas = canvasRef.current;
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext("2d");
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    const imageDataUrl = canvas.toDataURL("image/jpeg");
    setCapturedImage(imageDataUrl);
  };

  const retake = () => {
    setCapturedImage(null);
    setResult(null);
  };

  const submitVerification = async () => {
    setLoading(true);
    try {
      // Convert the captured base64 image into a File object for upload
      const blob = await (await fetch(capturedImage)).blob();
      const file = new File([blob], "capture.jpg", { type: "image/jpeg" });

      const formData = new FormData();
      formData.append("file", file);

      const res = await axiosClient.post(`/face/verify/${employee_id}`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResult(res.data);
    } catch (err) {
      setResult({ verified: false, message: "Verification request failed." });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 max-w-xl mx-auto space-y-6">
      <button onClick={() => navigate(-1)} className="text-accent-500 text-sm">
        ← Back
      </button>

      <div className="bg-navy-800 border border-navy-700 rounded-xl p-6 fade-in">
        <h2 className="text-xl font-bold text-white mb-1"> Critical Risk — Identity Verification</h2>
        <p className="text-gray-400 text-sm mb-4">
          Employee <span className="text-white">{employee_id}</span> triggered a Critical risk
          event. Please capture a webcam photo to confirm identity.
        </p>

        {cameraError && (
          <div className="bg-risk-critical/10 border border-risk-critical/40 text-risk-critical text-sm rounded-lg p-3 mb-4">
            {cameraError}
          </div>
        )}

        {!capturedImage ? (
          <>
            <video ref={videoRef} autoPlay className="w-full rounded-lg mb-4 bg-black" />
            <button
              onClick={capturePhoto}
              className="w-full bg-accent-600 hover:bg-accent-500 text-white py-2 rounded-lg font-semibold transition"
            >
               Capture Photo
            </button>
          </>
        ) : (
          <>
            <img src={capturedImage} alt="Captured" className="w-full rounded-lg mb-4" />
            <div className="flex gap-3">
              <button
                onClick={retake}
                className="flex-1 bg-navy-700 hover:bg-navy-600 text-white py-2 rounded-lg transition"
              >
                Retake
              </button>
              <button
                onClick={submitVerification}
                disabled={loading}
                className="flex-1 bg-accent-600 hover:bg-accent-500 text-white py-2 rounded-lg font-semibold transition disabled:opacity-50"
              >
                {loading ? "Verifying..." : "Submit for Verification"}
              </button>
            </div>
          </>
        )}

        {result && (
          <div
            className={`mt-4 p-4 rounded-lg text-sm ${
              result.verified
                ? "bg-risk-safe/10 border border-risk-safe/40 text-risk-safe"
                : "bg-risk-critical/10 border border-risk-critical/40 text-risk-critical"
            }`}
          >
            <p className="font-semibold">{result.message}</p>
            {result.distance !== null && result.distance !== undefined && (
              <p className="text-xs text-gray-400 mt-1">Distance score: {result.distance}</p>
            )}
          </div>
        )}

        {/* Hidden canvas used internally to capture a frame from the video */}
        <canvas ref={canvasRef} className="hidden" />
      </div>
    </div>
  );
}