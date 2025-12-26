import { useState } from "react";
import axios from "axios";

function App() {
  const [formFilled, setFormFilled] = useState(false);
  const [file, setFile] = useState(null);
  const [data, setData] = useState(null);
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (file) {
      setFormFilled(true);
    } else {
      alert("Please Upload Resume");
    }
    const formData = new FormData();
    formData.append("resume", file);
    const response = await axios.post(
      "https://resume-analyzer-9otw.onrender.com/api/resume/upload/",
      formData
    );

    if (response.status === 200) {
      const newResId = response.data.resume_id;
      const res = await axios.post(
        "https://resume-analyzer-9otw.onrender.com/api/resume/analyze/",
        { resume_id: newResId }
      );
      setData(res.data);
      console.log(res.data.matched_skills);
    }

    // console.log(response.data.resume_id)
  };

  return (
    <>
      <div className="main border w-[70%] m-auto flex flex-col items-center">
        {formFilled ? (
          <div className="inner-div border w-full">
            <h1 className="text-center text-2xl font-bold text-red-600 bg-yellow-400">
              Result
            </h1>
            <div>
              <span className="font-bold">Name:-</span>
              <span>{data?.detected_name}</span>
            </div>
            <div>
              <span className="font-bold">Role:-</span>
              <span>{data?.detected_role}</span>
            </div>
            <div>
              <span className="font-bold">Level:-</span>
              <span>{data?.experience_level}</span>
            </div>
            <div>
              <span className="font-bold">Match Score:-</span>
              <span>{data?.match_score}</span>
            </div>
            <div>
              <span className="font-bold">Matched Skills:-</span>
              <span>{data?.matched_skills.join(", ")}</span>
            </div>
            <div>
              <span className="font-bold">Missing Skills:-</span>
              <span>{data?.missing_skills.join(", ")}</span>
            </div>
            <div>
              <span className="font-bold">Suggetions:-</span>
              <span>{data?.suggetions}</span>
            </div>
          </div>
        ) : (
          <form
            onSubmit={handleSubmit}
            className="inline-flex flex-col items-center border gap-3"
          >
            <h1 className="bg-red-700 py-1 px-2 text-white font-bold">
              Upload Resume
            </h1>
            <input
              type="file"
              accept=".pdf"
              onChange={(e) => setFile(e.target.files[0])}
              className="border p-2 cursor-pointer"
            ></input>
            <button
              type="submit"
              className="bg-blue-800 text-yellow-300 font-bold py-1 px-3 cursor-pointer"
            >
              Submit
            </button>
          </form>
        )}
      </div>
    </>
  );
}

export default App;
