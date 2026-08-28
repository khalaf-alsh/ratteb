import { CheckCircle2, X } from "lucide-react";
import "./Toast.css";

type ToastProps = {
  message: string;
  onClose: () => void;
};

function Toast({ message, onClose }: ToastProps) {
  return (
    <div className="toast">
      <CheckCircle2 size={20} className="toast-icon" />

      <span className="toast-message">{message}</span>

      <button
        type="button"
        className="toast-close"
        onClick={onClose}
        aria-label="Close"
      >
        <X size={17} />
      </button>
    </div>
  );
}

export default Toast;
