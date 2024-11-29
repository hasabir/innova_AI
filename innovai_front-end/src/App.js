import "./App.css";
import React, { useState } from "react";
import TextareaAutosize from "react-textarea-autosize";

function App() {
    const [fileName, setFileName] = React.useState("");

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            setFileName(file.name);
        }
    };

    return (
        <div className="flex justify-center items-center h-screen">
            <div className="bg-[#ccdad1] w-[80%] h-[80vh] text-center flex justify-center items-center relative rounded-3xl container-shadow">
                <div>
                    <img
                        src="logo.png"
                        alt="logo"
                        className="w-36 h-36 absolute left-0 top-0 rounded-3xl"
                    />
                </div>
                <div className="flex flex-col w-1/2">
                    <label
                        htmlFor="query"
                        className="text-gray-500 text-base font-semibold mb-1 text-left"
                    >
                        Your Query <span className="text-red-500">*</span>
                    </label>
                    <TextareaAutosize
						minRows={2} 
                        id="query"
                        className="textarea textarea-primary text-base caret-secondary"
                        placeholder="Enter your query here"
                    />
                    <label
                        htmlFor="jobDescription"
                        className="text-gray-500 text-base font-semibold mt-2 mb-1 text-left"
                    >
                        Job Description (Optional)
                    </label>
                    <TextareaAutosize
						minRows={2} 
                        id="jobDescription"
                        className="textarea textarea-primary text-base caret-secondary"
                        placeholder="Enter job description here"
                    />
                    <div className="flex mt-4">
                        <button
                            className="btn btn-secondary mr-3"
                            type="submit"
                            value="Submit"
                        >
                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                fill="none"
                                viewBox="0 0 24 24"
                                strokeWidth={1.5}
                                stroke="currentColor"
                                className="size-6"
                            >
                                <path
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    d="M4.5 10.5 12 3m0 0 7.5 7.5M12 3v18"
                                />
                            </svg>
                            <span className="font-semibold text-base">
                                Submit
                            </span>
                        </button>
                        <label htmlFor="fileUpload" className="btn btn-accent">
                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                fill="none"
                                viewBox="0 0 24 24"
                                stroke-width="1.5"
                                stroke="currentColor"
                                class="size-5"
                            >
                                <path
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    d="m18.375 12.739-7.693 7.693a4.5 4.5 0 0 1-6.364-6.364l10.94-10.94A3 3 0 1 1 19.5 7.372L8.552 18.32m.009-.01-.01.01m5.699-9.941-7.81 7.81a1.5 1.5 0 0 0 2.112 2.13"
                                />
                            </svg>
                            <span className="font-semibold text-base">
                                Upload Resume
                            </span>
                        </label>
                        <input
                            id="fileUpload"
                            type="file"
                            className="hidden"
                            onChange={handleFileChange}
                        />
                        {fileName && (
                            <p className="text text-gray-500 ml-2 mt-3">
                                {fileName}
                            </p>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default App;
