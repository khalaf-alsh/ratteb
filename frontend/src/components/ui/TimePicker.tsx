import { useTranslation } from "react-i18next";
import "./TimePicker.css";

type TimePickerProps = {
  value: string;
  period: "am" | "pm";
  onTimeChange: (value: string) => void;
  onPeriodChange: (value: "am" | "pm") => void;
};

function TimePicker({
  value,
  period,
  onTimeChange,
  onPeriodChange,
}: TimePickerProps) {
  const { t } = useTranslation();

  const [hour = "", minute = ""] = value.split(":");

  const handleHourChange = (newHour: string) => {
    const numbersOnly = newHour.replace(/\D/g, "").slice(0, 2);
    onTimeChange(`${numbersOnly}:${minute}`);
  };

  const handleMinuteChange = (newMinute: string) => {
    const numbersOnly = newMinute.replace(/\D/g, "").slice(0, 2);
    onTimeChange(`${hour}:${numbersOnly}`);
  };

  return (
    <div className="time-picker">
      <div className="time-input-group">
        <input
          className="time-hour-input"
          type="text"
          inputMode="numeric"
          maxLength={2}
          value={hour}
          placeholder="05"
          onChange={(event) => handleHourChange(event.target.value)}
        />

        <span className="time-separator">:</span>

        <input
          className="time-minute-input"
          type="text"
          inputMode="numeric"
          maxLength={2}
          value={minute}
          placeholder="30"
          onChange={(event) => handleMinuteChange(event.target.value)}
        />
      </div>

      <select
        className="time-period-select"
        value={period}
        onChange={(event) => onPeriodChange(event.target.value as "am" | "pm")}
      >
        <option value="am">{t("am")}</option>
        <option value="pm">{t("pm")}</option>
      </select>
    </div>
  );
}

export default TimePicker;
