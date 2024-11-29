import "./App.css";
import React, { useState } from "react";
import TextareaAutosize from 'react-textarea-autosize';

function App() {
    const [fileName, setFileName] = React.useState("");

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            setFileName(file.name);
        }
    };

    return (
        <div className="bg-[#ccdad1] w-full h-screen text-center flex justify-center items-center">
            <div className="flex flex-col w-1/3">
				<TextareaAutosize className="textarea textarea-primary text-base caret-secondary" placeholder="Job Description" />
                <div className="flex mt-2">
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
                            className="size-5"
                        >
                            <path
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5m-13.5-9L12 3m0 0 4.5 4.5M12 3v13.5"
                            />
                        </svg>
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
    );
}

export default App;
