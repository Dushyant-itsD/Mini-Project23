import React, { useState } from "react";
import Navbar from '../SubComponents/Navbar';
import axios from "axios";

export default function Register() {
    const [fullName, setfullName] = useState("");
    const [email, setEmail] = useState("");
    const [Contact, setContact] = useState("");
    const [password, setPassword] = useState("");
    const [errorMessage, setErrorMessage] = useState("");
    const [successMessage, setSuccessMessage] = useState("");

    const handleSubmit = async (event) => {
        event.preventDefault();
        setErrorMessage("");  // Reset any previous error
        setSuccessMessage(""); // Reset success message

        try {
            const response = await axios.post('http://localhost:5000/users', {
                fullName,
                email,
                Contact,
                password,
            });

            console.log(response);
            setSuccessMessage("User registered successfully!");
            setTimeout(() => {
                window.location.href = "/login";
            }, 2000);

            // Reset form fields after successful submission
            setfullName("");
            setEmail("");
            setContact("");
            setPassword("");

        } catch (error) {
            console.error(error);
            setErrorMessage("Error occurred during registration. Please try again.");
        }
    };

    return (
        <>
            <Navbar />
            <div className="flex min-h-full flex-1 flex-col justify-center px-6 py-12 lg:px-8">
                <div className="sm:mx-auto sm:w-full sm:max-w-sm">
                    <h2 className="mt-10 text-center text-2xl/9 font-bold tracking-tight text-gray-900">
                        Sign in to your account
                    </h2>
                </div>

                <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
                    <form action="#" className="space-y-6" onSubmit={handleSubmit}>
                        <div>
                            <label htmlFor="name" className="block text-sm/6 font-medium text-gray-900">
                                Name
                            </label>
                            <div className="mt-2">
                                <input
                                    id="name"
                                    name="name"
                                    type="text"
                                    value={fullName}
                                    onChange={(e) => setfullName(e.target.value)}
                                    required
                                    autoComplete="name"
                                    className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm/6"
                                />
                            </div>
                        </div>

                        <div>
                            <label htmlFor="email" className="block text-sm/6 font-medium text-gray-900">
                                Email address
                            </label>
                            <div className="mt-2">
                                <input
                                    id="email"
                                    name="email"
                                    type="email"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    required
                                    autoComplete="email"
                                    className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm/6"
                                />
                            </div>
                        </div>

                        <div>
                            <label htmlFor="contact" className="block text-sm/6 font-medium text-gray-900">
                                Contact Number
                            </label>
                            <div className="mt-2">
                                <input
                                    id="contact"
                                    name="contact"
                                    type="tel"
                                    value={Contact}
                                    onChange={(e) => setContact(e.target.value)}
                                    required
                                    autoComplete="contact"
                                    maxLength="10"
                                    pattern="[0-9]{10}"
                                    title="Please enter a valid 10-digit contact number"
                                    className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm/6"
                                />
                            </div>
                        </div>

                        <div>
                            <div className="flex items-center justify-between">
                                <label htmlFor="password" className="block text-sm/6 font-medium text-gray-900">
                                    Password
                                </label>
                            </div>
                            <div className="mt-2">
                                <input
                                    id="password"
                                    name="password"
                                    type="password"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    required
                                    autoComplete="current-password"
                                    className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm/6"
                                />
                            </div>
                        </div>

                        {/* Display error or success messages */}
                        {errorMessage && <p className="text-red-500 text-sm">{errorMessage}</p>}
                        {successMessage && <p className="text-green-500 text-sm">{successMessage}</p>}

                        <div>
                            <button
                                type="submit"
                                className="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm/6 font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                            >
                                Sign up
                            </button>
                        </div>
                    </form>

                    <p className="mt-10 text-center text-sm/6 text-gray-500">
                        Not a member?{' '}
                        <a href="#" className="font-semibold text-indigo-600 hover:text-indigo-500">
                            Start a 14 day free trial
                        </a>
                    </p>
                </div>
            </div>
        </>
    );
}
