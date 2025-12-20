import { useState } from "react";

function App() {
  const [formFilled, setFormFilled] = useState(false);
  const [file, setFile] = useState(null);
  const handleSubmit = (e) => {
    e.preventDefault();
    if (file) {
      setFormFilled(true);
    } else {
      alert("Please Upload Resume");
    }
  };
  const formData = new FormData();
  formData.append("resume", file)
  const response=await axios.post()
  return (
    <>
      <div className="main border w-[70%] m-auto flex flex-col items-center">
        {formFilled ? (
          
            
            <div className="inner-div border w-full">
              <h1 className="text-center">Result</h1>
              <div>
                <span>Name:-</span>
              </div>
              <div>
                <span>Role:-</span>
              </div>
              <div>
                <span>Level:-</span>
              </div>
              <div>
                <span>Match Score:-</span>
              </div>
              <div>
                <span>Match Skills:-</span>
              </div>
              <div>
                <span>Missing Skills:-</span>
              </div>
              <div>
                <span>Suggetions:-</span>
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
