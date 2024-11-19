import './App.css';
import Home from './Component/Home'
import Login from './Component/Authorization/Login';
import Register from './Component/Authorization/Register';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
function App() {

  const router = createBrowserRouter([
    {
      path: "/",
      element: <Home />  
    },
   
    {
      path: "/login",
      element: <Login />  
    },
    {
      path: "/register",
      element: <Register />  
    }
  ]);

  return (
    <RouterProvider router={router} />
  );
}

export default App;
