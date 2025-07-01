import { Routes, Route, Navigate } from "react-router-dom";
import { lazy, Suspense } from "react";
import { CircularProgress, Box, Typography } from "@mui/material";
import PrivateRoute from "./PrivateRoute";
import Incident from "../Componenets/DispatchModule/IncidentCreate/Incident";
import SopRegister from "../Componenets/SuperAdmin/SOP/SopRegister";
import RegisterResponder from "../Componenets/SuperAdmin/Responder/RegisterResponder";
import ProtectedLoginRoute from "../Componenets/Login/ProtectedLoginRoute";
import IncidentReport from "../Componenets/SuperAdmin/Incident/IncidentReport";
const Login = lazy(() => import("../Componenets/Login/Login"));
const Sop = lazy(() => import("../Componenets/DispatchModule/SOP/Sop"));
const AlertPanel = lazy(() => import("../Componenets/DispatchModule/AlertPanel/AlertPanel"));
const AddDepartment = lazy(() => import("../Componenets/SuperAdmin/System/Department/AddDepartment"));
const AddGroup = lazy(() => import("../Componenets/SuperAdmin/System/Groups/Add_group"));
const AddEmployee = lazy(() => import("../Componenets/SuperAdmin/System/Employee_reg/Add_employee"));
const Map = lazy(() => import("../Componenets/DispatchModule/Map/Map"));
const MultiScreen = lazy(() => import("../Page/multiscreen"));
const ClosureDetail = lazy(() => import("../Componenets/SuperAdmin/Closure/ClosureDetail"));

const Loader = () => (
  <Box
    sx={{
      display: "flex",
      justifyContent: "center",
      alignItems: "center",
      height: "100vh",
    }}
  >
    <CircularProgress size={60} />
  </Box>
);

const Unauthorized = () => (
  <Box
    sx={{
      height: "100vh",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      flexDirection: "column",
    }}
  >
    <Typography variant="h3" color="error">
      401 - Unauthorized
    </Typography>
    <Typography variant="body1">
      You are not authorized to access this page.
    </Typography>
  </Box>
);

const AppRoutes = ({ darkMode, setIsLoggedIn }) => {
  return (
    <Suspense fallback={<Loader />}>
      <Routes>
        <Route path="/" element={<Navigate to="/login" />} />
        {/* <Route path="/login" element={<Login setIsLoggedIn={setIsLoggedIn} />} /> */}
        <Route
          path="/login"
          element={
            <ProtectedLoginRoute>
              <Login setIsLoggedIn={setIsLoggedIn} />
            </ProtectedLoginRoute>
          }
        />

        <Route
          path="/multiscreen"
          element={
            <PrivateRoute>
              <MultiScreen darkMode={darkMode} />
            </PrivateRoute>
          }
        />
        <Route
          path="/Map"
          element={
            <PrivateRoute>
              <Map darkMode={darkMode} />
            </PrivateRoute>
          }
        />
        <Route
          path="/alert-panel"
          element={
            <PrivateRoute>
              <AlertPanel darkMode={darkMode} />
            </PrivateRoute>
          }
        />
        <Route
          path="/sop"
          element={
            <PrivateRoute>
              <Sop darkMode={darkMode} />
            </PrivateRoute>
          }
        />
        <Route
          path="/add-department"
          element={
            <PrivateRoute>
              <AddDepartment darkMode={darkMode} />
            </PrivateRoute>
          }
        />
        <Route
          path="/add-group"
          element={
            <PrivateRoute>
              <AddGroup darkMode={darkMode} />
            </PrivateRoute>
          }
        />
        <Route
          path="/add-employee"
          element={
            <PrivateRoute>
              <AddEmployee darkMode={darkMode} />
            </PrivateRoute>
          }
        />
        <Route
          path="/create-incident"
          element={
            <PrivateRoute>
              <Incident darkMode={darkMode} />
            </PrivateRoute>
          }
        />
        <Route
          path="/Register Sop"
          element={
            <PrivateRoute>
              <SopRegister darkMode={darkMode} />
            </PrivateRoute>
          }
        />
        <Route
          path="/Responder"
          element={
            <PrivateRoute>
              <RegisterResponder darkMode={darkMode} />
            </PrivateRoute>
          }
        />
        <Route
          path="/Closure Report"
          element={
            <PrivateRoute>
              <ClosureDetail darkMode={darkMode} />
            </PrivateRoute>
          }
        />
         <Route
          path="/Incident Report"
          element={
            <PrivateRoute>
              <IncidentReport darkMode={darkMode} />
            </PrivateRoute>
          }
        />

        <Route path="*" element={<Unauthorized />} />
      </Routes>
    </Suspense>
  );
};

export default AppRoutes;
