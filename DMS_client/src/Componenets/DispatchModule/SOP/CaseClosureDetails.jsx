import {
  Paper,
  Grid,
  Typography,
  TextField,
  Skeleton,
  Box,
  Button,
  CircularProgress,
  Alert,
  Select,
  MenuItem,
  Checkbox,
  ListItemText,
} from "@mui/material";
import axios from "axios";
import { useEffect, useState } from "react";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import { AdapterDateFns } from "@mui/x-date-pickers/AdapterDateFns";
import { DateTimePicker } from "@mui/x-date-pickers/DateTimePicker";
import { useAuth } from "../../../Context/ContextAPI";
import { Tooltip } from "@mui/material";

const CaseClosureDetails = ({
  darkMode,
  flag,
  selectedIncident,
  fetchDispatchList,
}) => {
  const port = import.meta.env.VITE_APP_API_KEY;
  const token = localStorage.getItem("accessToken");
  const userName = localStorage.getItem("userId");
  const {
    selectedIncidentFromSop,
    disasterIdFromSop,
    setSelectedIncidentFromSop,
  } = useAuth();
  console.log(
    "disater name and inc_id from sop",
    selectedIncidentFromSop,
    disasterIdFromSop
  );

  window.addEventListener('storage', (e) => {
    if (e.key === 'logout') {
      location.href = '/login';
    }
  });


  console.log("selectedIncidentselectedIncident", selectedIncident);

  const [isDataCleared, setIsDataCleared] = useState(false);
  const [validationErrors, setValidationErrors] = useState({});

  // New state for responder list
  const [responderList, setResponderList] = useState([]);
  const [responderLoading, setResponderLoading] = useState(false);
  const [responderError, setResponderError] = useState(null);

  // Function to fetch responder list
  const fetchResponderList = async (inc_id) => {
    if (!inc_id) return;

    try {
      setResponderLoading(true);
      setResponderError(null);

      const authToken = localStorage.getItem("access_token") || token;
      const response = await axios.get(
        `${port}/admin_web/get_responder_list/${inc_id}`,
        {
          headers: {
            Authorization: `Bearer ${authToken}`,
            "Content-Type": "application/json",
          },
        }
      );

      console.log("Responder API Response:", response.data);

      // Assuming the API returns responder data in response.data
      // Adjust this based on your actual API response structure
      if (response.data && Array.isArray(response.data)) {
        setResponderList(response.data);
      } else if (response.data && response.data.responders) {
        setResponderList(response.data.responders);
      } else {
        setResponderList([]);
      }

    } catch (error) {
      console.error("Error fetching responder list:", error);
      setResponderError(error.response?.data?.message || "Failed to fetch responder list");
      setResponderList([]);
    } finally {
      setResponderLoading(false);
    }
  };

  // Fetch responder list when incidentId changes
  useEffect(() => {
    const currentIncId = selectedIncidentFromSop?.inc_id || selectedIncident?.inc_id;

    if (currentIncId) {
      console.log("Fetching responder list for inc_id:", currentIncId);
      fetchResponderList(currentIncId);
    }
  }, [selectedIncidentFromSop, selectedIncident]);

  const validateForm = () => {
    const errors = {};

    // Responder Scope
    if (!selectedDepartments || selectedDepartments.length === 0) {
      errors.selectedDepartments = "Responder Scope is required";
    }

    // Vehicle Number
    if (!formData.vehicleNumber) {
      errors.vehicleNumber = "Vehicle Number is required";
    } else {
      const value = formData.vehicleNumber.replace(/-/g, '');
      const vehicleRegex = /^[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}$/;
      if (value && !vehicleRegex.test(value)) {
        errors.vehicleNumber = "Invalid format";
      }
    }

    // Responder Name
    if (!formData.responderName || !formData.responderName.trim()) {
      errors.responderName = "Responder Name is required";
    }

    // Date fields
    if (!formData.acknowledge) errors.acknowledge = "Acknowledge is required";
    if (!formData.startBaseLocation) errors.startBaseLocation = "Start Base Location is required";
    if (!formData.atScene) errors.atScene = "At Scene is required";
    if (!formData.fromScene) errors.fromScene = "From Scene is required";
    if (!formData.backToBase) errors.backToBase = "Back to Base is required";

    // Closure Remark
    if (!formData.closureRemark || !formData.closureRemark.trim()) {
      errors.closureRemark = "Remark is required";
    }

    setValidationErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const [formData, setFormData] = useState({
    responderName: "",
    vehicleNumber: "",
    acknowledge: "",
    startBaseLocation: "",
    atScene: "",
    fromScene: "",
    backToBase: "",
    closureRemark: "",
  });

  const [loading, setLoading] = useState(false);
  const [submitStatus, setSubmitStatus] = useState(null);

  const labelColor = darkMode ? "rgb(95,200,236)" : "rgb(95,200,236)";
  const textColor = darkMode ? "#ffffff" : "#000000";
  const fontFamily = "Roboto, sans-serif";
  const borderColor = darkMode ? "#7F7F7F" : "#e0e0e0";
  const [remark, setRemark] = useState("");
  const toISOString = (datetime) => {
    if (!datetime) return null;
    const date = new Date(datetime);
    return date.toISOString(); // returns like "2025-05-29T10:00:00.000Z"
  };

  const [timestamps, setTimestamps] = useState({
    acknowledge: "",
    startBaseLocation: "",
    atScene: "",
    fromScene: "",
    backToBase: "",
  });
  // Load initial values from props

  // useEffect(() => {
  //   if (selectedIncident) {
  //     setTimestamps({
  //       acknowledge: formatDateTimeLocal(selectedIncident.acknowledge),
  //       startBaseLocation: formatDateTimeLocal(
  //         selectedIncident.startBaseLocation
  //       ),
  //       atScene: formatDateTimeLocal(selectedIncident.atScene),
  //       fromScene: formatDateTimeLocal(selectedIncident.fromScene),
  //       backToBase: formatDateTimeLocal(selectedIncident.backToBase),
  //     });
  //   }
  // }, [selectedIncident]);

  // const handleChange = (key, value) => {
  //   setTimestamps((prev) => ({ ...prev, [key]: value }));
  // };

  const textFieldStyle = {
    "& .MuiInputLabel-root": { color: labelColor },
    "& .MuiOutlinedInput-root": {
      backgroundColor: darkMode ? "#202328" : "#FFFFFF",
      borderRadius: 2,
    },
  };

  // Load data when selectedIncident changes
  useEffect(() => {
    if (selectedIncident) {
      setFormData({
        acknowledge: selectedIncident.acknowledge || "",
        startBaseLocation: selectedIncident.startBaseLocation || "",
        atScene: selectedIncident.atScene || "",
        fromScene: selectedIncident.fromScene || "",
        backToBase: selectedIncident.backToBase || "",
        closureRemark: selectedIncident.closureRemark || "",
      });
    }
  }, [selectedIncident]);

  const handleChange = (field, value) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  const formatDate = (date) => {
    if (!date) return "";
    const d = new Date(date);
    const pad = (n) => (n < 10 ? "0" + n : n);
    return (
      d.getFullYear() +
      "-" +
      pad(d.getMonth() + 1) +
      "-" +
      pad(d.getDate()) +
      " " +
      pad(d.getHours()) +
      ":" +
      pad(d.getMinutes()) +
      ":" +
      pad(d.getSeconds())
    );
  };

  const handleSubmit = async () => {
    if (!validateForm()) {
      setSubmitStatus({
        type: "error",
        message: "Please fill all required fields",
      });
      return;
    }

    // Check if we have incident data
    const numericIncId = selectedIncidentFromSop?.inc_id || selectedIncident?.inc_id;
    const incidentId =
      selectedIncidentFromSop?.incident_id || selectedIncident?.incident_id;


    if (!numericIncId) {
      setSubmitStatus({ type: "error", message: "No incident ID found!" });
      return;
    }

    const payload = {
      incident_id: incidentId,
      inc_id: numericIncId,
      // responder: selectedDepartments.length > 0 ? selectedDepartments[0] : "", 
      responder: selectedDepartments, 
      closure_responder_name: formData.responderName || "", 
      vehicle_no: formData.vehicleNumber,
      closure_acknowledge: formData.acknowledge ? formatDate(formData.acknowledge) : "",
      closure_start_base_location: formData.startBaseLocation ? formatDate(formData.startBaseLocation) : "",
      closure_at_scene: formData.atScene ? formatDate(formData.atScene) : "",
      closure_from_scene: formData.fromScene ? formatDate(formData.fromScene) : "",
      closure_back_to_base: formData.backToBase ? formatDate(formData.backToBase) : "",
      // incident_responder_by: selectedDepartments,
      closure_added_by: userName,
      closure_modified_by: userName,
      closure_modified_date: new Date().toISOString(), 
      closure_remark: formData.closureRemark,
    };

    console.log("Payload being sent:", payload);

    try {
      setLoading(true);
      setSubmitStatus(null);

      const authToken = localStorage.getItem("access_token") || token;

      const res = await axios.post(
        `${port}/admin_web/closure_post_api/`,
        payload,
        {
          headers: {
            Authorization: `Bearer ${authToken}`,
            "Content-Type": "application/json",
          },
        }
      );

      console.log("API Response:", res.data);
      setSubmitStatus({
        type: "success",
        message: "Closure details saved successfully!",
      });

      // Check if API response has remaining departments
      const remainingDepartments = res.data.Departments || [];

      // Update selectedDepartments with remaining departments from API response
      setSelectedDepartments(remainingDepartments);
      if (remainingDepartments.length === 0) {
        setFormData({
          vehicleNumber: "",
          responderName: "",
          acknowledge: "",
          startBaseLocation: "",
          atScene: "",
          fromScene: "",
          backToBase: "",
          closureRemark: "",
        });
        setSelectedIncidentFromSop(null);
        setIsDataCleared(true);
        fetchDispatchList();
        await fetchResponderList();
      } else {
        // If departments are still pending, only clear vehicle and responder specific fields
        setFormData(prev => ({
          ...prev,
          vehicleNumber: "",
          responderName: "",
          closureRemark: "",
          acknowledge: "",
          startBaseLocation: "",
          atScene: "",
          fromScene: "",
          backToBase: "",
          // Keep the datetime fields as they are likely same for all responders
        }));
        await fetchResponderList();

      }

    } catch (error) {
      console.error("API Error:", error);
      console.error("Error response:", error.response?.data);

      const errorMessage =
        error.response?.data?.message ||
        error.response?.data?.error ||
        "Failed to save closure details.";

      setSubmitStatus({ type: "error", message: errorMessage });
    } finally {
      setLoading(false);
    }
  };

  // Inside your component
  useEffect(() => {
    if (submitStatus) {
      const timer = setTimeout(() => {
        setSubmitStatus(null);
      }, 3000);

      return () => clearTimeout(timer);
    }
  }, [submitStatus]);

  const getAlertTypeName = (alertType) => {
    const alertTypeMap = {
      1: "High",
      2: "Medium",
      3: "Low",
      4: "Very Low",
    };
    return alertTypeMap[alertType] || "Unknown";
  };
  const renderText = (label, value, index, total) => (
    <Box
      sx={{
        pb: 1.5,
        mb: 1.5,
        mr: 2,
        borderBottom: index === total - 1 ? "none" : `1px solid ${borderColor}`,
      }}
    >
      <Typography
        variant="body2"
        sx={{ color: labelColor, fontWeight: 500, fontFamily }}
      >
        {label}
      </Typography>
      {selectedIncident ? (
        <Typography variant="body2" sx={{ fontFamily, color: textColor }}>
          {value || "N/A"}
        </Typography>
      ) : (
        <Skeleton variant="text" width={120} height={24} />
      )}
    </Box>
  );

  const [selectedDepartments, setSelectedDepartments] = useState([]);

  const handleChange1 = (event) => {
    setSelectedDepartments(event.target.value);
  };

  return (
    <>
      {submitStatus && (
        <Box
          sx={{
            width: "100%",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            height: "auto",
            margin: 0,
            padding: 0,
          }}
        >
          <Alert severity={submitStatus.type}>{submitStatus.message}</Alert>
        </Box>
      )}

      <Typography
        variant="h6"
        sx={{
          fontFamily,
          mb: 2,
          ml: 1,
          fontWeight: 500,
          color: labelColor,
        }}
      >
        Case Closure Details
      </Typography>

      <Paper
        elevation={3}
        sx={{
          p: 2,
          mb: 5,
          borderRadius: 2,
          backgroundColor: darkMode ? "#121212" : "#FFFFFF",
          color: textColor,
          transition: "all 0.3s ease",
        }}
      >
        <Grid container spacing={1} sx={{ height: "300px" }}>
          {/* Left Column - Incident Info (Reduced width) */}
          <Grid
            item
            xs={12}
            md={3.3}
            sx={{
              // mt: 1,
              mb: 0.5,
              borderRight: { md: `1px solid ${borderColor}` },
              pr: { md: 3 },
            }}
          >
            <Typography
              variant="subtitle1"
              sx={{
                fontWeight: 500,
                color: labelColor,
                fontFamily,
                mb: 2,
                textAlign: "left",
                // borderBottom: `2px solid ${labelColor}`,
                // pb: 1
              }}
            >
              Incident Info
            </Typography>

            <Box
              sx={{
                height: "250px",
                overflowY: "auto",
                "&::-webkit-scrollbar": {
                  width: "6px",
                },
                "&::-webkit-scrollbar-track": {
                  background: darkMode ? "#2e2e2e" : "#f1f1f1",
                  borderRadius: "3px",
                  marginTop: "1rem",
                },
                "&::-webkit-scrollbar-thumb": {
                  background: darkMode ? "#555" : "#888",
                  borderRadius: "3px",
                },
                "&::-webkit-scrollbar-thumb:hover": {
                  background: darkMode ? "#777" : "#555",
                },
              }}
            >
              {flag === 0 ? (
                <Box
                  sx={{
                    scrollBehavior: "smooth",
                    "&::-webkit-scrollbar": {
                      width: "6px",
                    },
                    "&::-webkit-scrollbar-thumb": {
                      backgroundColor: darkMode ? "#0288d1" : "#888",
                      borderRadius: 3,
                    },
                    "&::-webkit-scrollbar-thumb:hover": {
                      backgroundColor: darkMode ? "#5FC8EC" : "#555",
                    },
                  }}
                >
                  <Grid container spacing={2}>
                    <Grid item xs={12} md={6}>
                      <Box>
                        <Typography
                          variant="body2"
                          sx={{
                            color: labelColor,
                            fontWeight: 500,
                            fontFamily,
                          }}
                        >
                          Caller Name
                        </Typography>
                        <Typography
                          variant="subtitle2"
                          sx={{
                            fontFamily,
                            color: textColor,
                            wordBreak: "break-word",
                          }}
                        >
                          {selectedIncidentFromSop?.incident_details?.[0]?.caller_name || "N/A"}
                        </Typography>
                      </Box>
                    </Grid>

                    <Grid item xs={12} md={6}>
                      <Box>
                        <Typography
                          variant="body2"
                          sx={{
                            color: labelColor,
                            fontWeight: 500,
                            fontFamily,
                          }}
                        >
                          Caller Number
                        </Typography>
                        <Typography
                          variant="subtitle2"
                          sx={{
                            fontFamily,
                            color: textColor,
                            wordBreak: "break-word",
                          }}
                        >
                          {selectedIncidentFromSop?.incident_details?.[0]?.caller_no || "N/A"}
                        </Typography>
                      </Box>
                    </Grid>

                    <Grid item xs={12} md={6}>
                      <Box>
                        <Typography
                          variant="body2"
                          sx={{
                            color: labelColor,
                            fontWeight: 500,
                            fontFamily,
                          }}
                        >
                          District
                        </Typography>
                        <Typography
                          variant="subtitle2"
                          sx={{
                            fontFamily,
                            color: textColor,
                            wordBreak: "break-word",
                          }}
                        >
                          {selectedIncidentFromSop?.incident_details?.[0]?.district_name || "N/A"}
                        </Typography>
                      </Box>
                    </Grid>

                    <Grid item xs={12} md={6}>
                      <Box>
                        <Typography
                          variant="body2"
                          sx={{
                            color: labelColor,
                            fontWeight: 500,
                            fontFamily,
                          }}
                        >
                          Tehsil
                        </Typography>
                        <Typography
                          variant="subtitle2"
                          sx={{
                            fontFamily,
                            color: textColor,
                            wordBreak: "break-word",
                          }}
                        >
                          {selectedIncidentFromSop?.incident_details?.[0]?.tahsil_name || "N/A"}
                        </Typography>
                      </Box>
                    </Grid>

                    <Grid item xs={12} md={6}>
                      <Box>
                        <Typography
                          variant="body2"
                          sx={{
                            color: labelColor,
                            fontWeight: 500,
                            fontFamily,
                          }}
                        >
                          Ward
                        </Typography>
                        <Typography
                          variant="subtitle2"
                          sx={{
                            fontFamily,
                            color: textColor,
                            wordBreak: "break-word",
                          }}
                        >
                          {selectedIncidentFromSop?.incident_details?.[0]?.ward_name || "N/A"}
                        </Typography>
                      </Box>
                    </Grid>

                    <Grid item xs={12} md={6}>
                      <Box>
                        <Typography
                          variant="body2"
                          sx={{
                            color: labelColor,
                            fontWeight: 500,
                            fontFamily,
                          }}
                        >
                          Ward Officer
                        </Typography>
                        <Typography
                          variant="subtitle2"
                          sx={{
                            fontFamily,
                            color: textColor,
                            wordBreak: "break-word",
                          }}
                        >
                          {selectedIncidentFromSop?.incident_details?.[0]?.ward_officer_name &&
                            selectedIncidentFromSop.incident_details[0].ward_officer_name.length > 0
                            ? selectedIncidentFromSop.incident_details[0].ward_officer_name.map((officer, idx) => {
                              const name = officer.ward_officer_name;
                              const displayName = name.length > 15 ? name.slice(0, 15) + "..." : name;
                              return (
                                <Tooltip key={officer.emp_id} title={name.length > 15 ? name : ""} arrow>
                                  <span>
                                    {displayName}
                                    {idx !== selectedIncidentFromSop.incident_details[0].ward_officer_name.length - 1 ? ", " : ""}
                                  </span>
                                </Tooltip>
                              );
                            })
                            : "N/A"}
                        </Typography>
                      </Box>
                    </Grid>

                    <Grid item xs={12} md={12}>
                      <Box>
                        <Typography
                          variant="body2"
                          sx={{
                            color: labelColor,
                            fontWeight: 500,
                            fontFamily,
                          }}
                        >
                          Location
                        </Typography>
                        <Typography
                          variant="subtitle2"
                          sx={{
                            fontFamily,
                            color: textColor,
                            wordBreak: "break-word",
                          }}
                        >
                          {(() => {
                            const location = selectedIncidentFromSop?.incident_details?.[0]?.location || "N/A";
                            const showTooltip = location !== "N/A" && location.length > 40;
                            const displayLocation = showTooltip ? location.slice(0, 40) + "..." : location;
                            return showTooltip ? (
                              <Tooltip title={location} arrow>
                                <span>{displayLocation}</span>
                              </Tooltip>
                            ) : (
                              location
                            );
                          })()}
                        </Typography>
                      </Box>
                    </Grid>

                    <Grid item xs={12} md={12}>
                      <Box>
                        <Typography
                          variant="body2"
                          sx={{
                            color: labelColor,
                            fontWeight: 500,
                            fontFamily,
                          }}
                        >
                          Summary
                        </Typography>
                        <Typography
                          variant="subtitle2"
                          sx={{
                            fontFamily,
                            color: textColor,
                            wordBreak: "break-word",
                          }}
                        >
                          {(() => {
                            const summary = selectedIncidentFromSop?.incident_details?.[0]?.summary_name || "N/A";
                            const showTooltip = summary !== "N/A" && summary.length > 50;
                            const displaySummary = showTooltip ? summary.slice(0, 50) + "..." : summary;
                            return showTooltip ? (
                              <Tooltip title={summary} arrow>
                                <span>{displaySummary}</span>
                              </Tooltip>
                            ) : (
                              summary
                            );
                          })()}
                        </Typography>
                      </Box>
                    </Grid>
                  </Grid>
                </Box>
              ) : (
                <Typography
                  variant="body2"
                  sx={{ color: textColor, textAlign: "center", mt: 4 }}
                >
                  No incident data to display.
                </Typography>
              )}
            </Box>
          </Grid>

          {/* Middle Column - Case Timeline (Increased width) */}
          <Grid
            item
            xs={12}
            md={4.7}
            sx={{
              // mt: 1,
              mb: 0.5,
              borderRight: { md: `1px solid ${borderColor}` },
              px: { md: 3 },
            }}
          >
            <Typography
              variant="subtitle1"
              sx={{
                fontWeight: 500,
                color: labelColor,
                fontFamily,
                // mb: 2,
                textAlign: "left",
                // borderBottom: `2px solid ${labelColor}`,
                // pb: 1
              }}
            >
              Case Timeline
            </Typography>

            <Box
              sx={{
                height: "250px",
                overflowY: "auto",
                "&::-webkit-scrollbar": {
                  width: "6px",
                },
                "&::-webkit-scrollbar-track": {
                  background: darkMode ? "#2e2e2e" : "#f1f1f1",
                  borderRadius: "3px",
                  marginTop: "1rem",
                },
                "&::-webkit-scrollbar-thumb": {
                  background: darkMode ? "#555" : "#888",
                  borderRadius: "3px",
                },
                "&::-webkit-scrollbar-thumb:hover": {
                  background: darkMode ? "#777" : "#555",
                },
              }}
            >
              <Grid container spacing={2} sx={{ mt: 0.6 }}>
                <Grid item xs={6}>
                  <Select
                    displayEmpty
                    value={selectedDepartments}
                    onChange={(event) => {
                      setSelectedDepartments(event.target.value);
                      if (validationErrors.selectedDepartments) {
                        setValidationErrors((prev) => ({
                          ...prev,
                          selectedDepartments: null,
                        }));
                      }
                    }}
                    renderValue={(selected) => {
                      if (!selected) {
                        return (
                          <span style={{ color: "#888", fontStyle: "normal" }}>
                            {responderLoading ? "Loading..." : "Responder Scope"}
                          </span>
                        );
                      }
                      return selected;
                    }}
                    size="small"
                    fullWidth
                    disabled={responderLoading}
                    inputProps={{ "aria-label": "Select Responder" }}
                    MenuProps={{
                      PaperProps: {
                        style: {
                          maxHeight: 250,
                          width: 200,
                        },
                      },
                    }}
                    error={!!validationErrors.selectedDepartments}
                    sx={validationErrors.selectedDepartments ? { border: '1px solid #d32f2f', borderRadius: 1 } : {}}
                  >
                    <MenuItem disabled value="">
                      <em>
                        {responderLoading
                          ? "Loading responders..."
                          : responderError
                            ? "Error loading responders"
                            : "Select Responder Scope"
                        }
                      </em>
                    </MenuItem>

                    {responderList.map((responder, index) => (
                      <MenuItem
                        key={responder.responder_id || index}
                        value={responder.responder_name || responder.name}
                      >
                        {responder.responder_name || responder.name}
                      </MenuItem>
                    ))}
                  </Select>

                  {(validationErrors.selectedDepartments || responderError) && (
                    <Typography
                      variant="caption"
                      color="error"
                      sx={{ mt: 0.5, display: 'block' }}
                    >
                      {validationErrors.selectedDepartments || responderError}
                    </Typography>
                  )}
                </Grid>

                <Grid item xs={6}>
                  <TextField
                    id="outlined-basic"
                    label="Vehicle Number"
                    variant="outlined"
                    size="small"
                    placeholder="Eg.MH-12-AB-1234"
                    value={formData.vehicleNumber || ''}
                    onChange={(e) => {
                      const value = e.target.value.toUpperCase();
                      // Allow only alphanumeric characters and hyphens, limit to 13 characters
                      const filteredValue = value.replace(/[^A-Z0-9-]/g, '').slice(0, 13);
                      handleChange("vehicleNumber", filteredValue);

                      // Clear validation error when user starts typing
                      if (validationErrors.vehicleNumber) {
                        setValidationErrors((prev) => ({
                          ...prev,
                          vehicleNumber: null,
                        }));
                      }
                    }}
                    onBlur={(e) => {
                      const value = e.target.value.replace(/-/g, ''); // Remove hyphens for validation
                      // Validate both formats: MH12AB1234 and MH12A1234
                      const vehicleRegex = /^[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}$/;

                      if (value && !vehicleRegex.test(value)) {
                        setValidationErrors((prev) => ({
                          ...prev,
                          vehicleNumber: "Invalid format",
                        }));
                      }
                    }}
                    error={!!validationErrors.vehicleNumber}
                    helperText={validationErrors.vehicleNumber}
                    InputProps={{
                      sx: {
                        color: textColor,
                        textTransform: 'uppercase'
                      }
                    }}
                  // sx={textFieldStyle}
                  />
                </Grid>

                <Grid item xs={6}>
                  <TextField
                    id="responder-name-field"
                    label="Responder Name"
                    variant="outlined"
                    size="small"
                    value={formData.responderName || ''}
                    onChange={(e) => {
                      const value = e.target.value;
                      setFormData(prev => ({
                        ...prev,
                        responderName: value
                      }));

                      // Clear validation error if exists
                      if (validationErrors.responderName) {
                        setValidationErrors((prev) => ({
                          ...prev,
                          responderName: null,
                        }));
                      }
                    }}
                    onBlur={(e) => {
                      // Show error if left empty on blur
                      if (!e.target.value.trim()) {
                        setValidationErrors((prev) => ({
                          ...prev,
                          responderName: "Responder Name is required",
                        }));
                      }
                    }}
                    placeholder="Enter responder name"
                    error={!!validationErrors.responderName}
                    helperText={validationErrors.responderName}
                    InputProps={{
                      sx: {
                        color: textColor,
                      }
                    }}
                  // sx={textFieldStyle}
                  />
                </Grid>

                <LocalizationProvider dateAdapter={AdapterDateFns}>
                  <Grid item xs={6}>
                    <DateTimePicker
                      label="Acknowledge"
                      value={formData.acknowledge || null}
                      onChange={(newValue) => {
                        handleChange("acknowledge", newValue);
                        if (validationErrors.acknowledge) {
                          setValidationErrors((prev) => ({
                            ...prev,
                            acknowledge: null,
                          }));
                        }
                      }}
                      ampm={false}
                      minDateTime={selectedIncidentFromSop?.incident_details?.[0]?.inc_datetime ?
                        new Date(selectedIncidentFromSop.incident_details[0].inc_datetime) :
                        new Date()
                      }
                      inputFormat="yyyy-MM-dd | HH:mm"
                      views={["year", "month", "day", "hours", "minutes"]}
                      slotProps={{
                        textField: {
                          size: 'small',
                          required: true,
                          error: !!validationErrors.acknowledge,
                          helperText: validationErrors.acknowledge,
                          fullWidth: true,
                          placeholder: "yyyy-MM-dd | hh:mm",
                          InputLabelProps: { shrink: true },
                          InputProps: {
                            sx: {
                              color: textColor,
                              height: "35px",
                              "& .MuiSvgIcon-root": {
                                color: "white",
                              },
                            },
                          },
                          sx: textFieldStyle,
                        }
                      }}
                    />
                  </Grid>

                  <Grid item xs={6}>
                    <DateTimePicker
                      label="Start Location"
                      value={formData.startBaseLocation || null}
                      onChange={(newValue) => {
                        handleChange("startBaseLocation", newValue);
                        if (validationErrors.startBaseLocation) {
                          setValidationErrors((prev) => ({
                            ...prev,
                            startBaseLocation: null,
                          }));
                        }
                      }}
                      ampm={false}
                      minDateTime={
                        formData.acknowledge ||
                        (selectedIncidentFromSop?.incident_details?.[0]?.inc_datetime
                          ? new Date(selectedIncidentFromSop.incident_details[0].inc_datetime)
                          : new Date())
                      }
                      inputFormat="yyyy-MM-dd | HH:mm"
                      slotProps={{
                        textField: {
                          size: 'small',
                          required: true,
                          error: !!validationErrors.startBaseLocation,
                          helperText: validationErrors.startBaseLocation,
                          fullWidth: true,
                          placeholder: "yyyy-MM-dd | hh:mm",
                          InputLabelProps: { shrink: true },
                          InputProps: {
                            sx: {
                              color: textColor,
                              height: "35px",
                              "& .MuiSvgIcon-root": {
                                color: "white",
                              },
                            },
                          },
                          sx: textFieldStyle,
                        }
                      }}
                    />
                  </Grid>

                  <Grid item xs={6}>
                    <DateTimePicker
                      label="At Scene"
                      value={formData.atScene || null}
                      onChange={(newValue) => {
                        handleChange("atScene", newValue);
                        if (validationErrors.atScene) {
                          setValidationErrors((prev) => ({
                            ...prev,
                            atScene: null,
                          }));
                        }
                      }}
                      ampm={false}
                      minDateTime={
                        formData.acknowledge ||
                        (selectedIncidentFromSop?.incident_details?.[0]?.inc_datetime
                          ? new Date(selectedIncidentFromSop.incident_details[0].inc_datetime)
                          : new Date())
                      }
                      inputFormat="yyyy-MM-dd | HH:mm"
                      slotProps={{
                        textField: {
                          size: 'small',
                          required: true,
                          error: !!validationErrors.atScene,
                          helperText: validationErrors.atScene,
                          fullWidth: true,
                          placeholder: "yyyy-MM-dd | hh:mm",
                          InputLabelProps: { shrink: true },
                          InputProps: {
                            sx: {
                              color: textColor,
                              height: "35px",
                              fontSize: "0.85rem",
                              "& .MuiSvgIcon-root": {
                                color: "white",
                              },
                            },
                          },
                          sx: textFieldStyle,
                        }
                      }}
                    />
                  </Grid>

                  <Grid item xs={6}>
                    <DateTimePicker
                      label="From Scene"
                      value={formData.fromScene || null}
                      onChange={(newValue) => {
                        handleChange("fromScene", newValue);
                        if (validationErrors.fromScene) {
                          setValidationErrors((prev) => ({
                            ...prev,
                            fromScene: null,
                          }));
                        }
                      }}
                      ampm={false}
                      minDateTime={
                        formData.acknowledge ||
                        (selectedIncidentFromSop?.incident_details?.[0]?.inc_datetime
                          ? new Date(selectedIncidentFromSop.incident_details[0].inc_datetime)
                          : new Date())
                      }
                      inputFormat="yyyy-MM-dd | HH:mm"
                      slotProps={{
                        textField: {
                          size: 'small',
                          required: true,
                          error: !!validationErrors.fromScene,
                          helperText: validationErrors.fromScene,
                          fullWidth: true,
                          placeholder: "yyyy-MM-dd | hh:mm",
                          InputLabelProps: { shrink: true },
                          InputProps: {
                            sx: {
                              color: textColor,
                              height: "35px",
                              fontSize: "0.85rem",
                              "& .MuiSvgIcon-root": {
                                color: "white",
                              },
                            },
                          },
                          sx: textFieldStyle,
                        }
                      }}
                    />
                  </Grid>

                  <Grid item xs={6}>
                    <DateTimePicker
                      label="Back to Base"
                      value={formData.backToBase || null}
                      onChange={(newValue) => {
                        handleChange("backToBase", newValue);
                        if (validationErrors.backToBase) {
                          setValidationErrors((prev) => ({
                            ...prev,
                            backToBase: null,
                          }));
                        }
                      }}
                      ampm={false}
                      minDateTime={
                        formData.acknowledge ||
                        (selectedIncidentFromSop?.incident_details?.[0]?.inc_datetime
                          ? new Date(selectedIncidentFromSop.incident_details[0].inc_datetime)
                          : new Date())
                      }
                      inputFormat="yyyy-MM-dd | HH:mm"
                      slotProps={{
                        textField: {
                          size: 'small',
                          required: true,
                          error: !!validationErrors.backToBase,
                          helperText: validationErrors.backToBase,
                          fullWidth: true,
                          placeholder: "yyyy-MM-dd | hh:mm",
                          InputLabelProps: { shrink: true },
                          InputProps: {
                            sx: {
                              color: textColor,
                              height: "35px",
                              fontSize: "0.85rem",
                              "& .MuiSvgIcon-root": {
                                color: "white",
                              },
                            },
                          },
                          sx: textFieldStyle,
                        }
                      }}
                    />
                  </Grid>
                </LocalizationProvider>
              </Grid>
            </Box>
          </Grid>

          {/* Right Column - Closure Remark */}
          <Grid item xs={12} md={4}>
            <Typography
              variant="subtitle1"
              sx={{
                fontWeight: 500,
                color: labelColor,
                fontFamily,
                // mb: 2,
                textAlign: "left",
                // borderBottom: `2px solid ${labelColor}`,
                // pb: 1
              }}
            >
              Closure Remark
            </Typography>

            <Box
              sx={{
                height: "250px",
                // overflowY: "auto",
                "&::-webkit-scrollbar": {
                  width: "6px",
                },
                "&::-webkit-scrollbar-track": {
                  background: darkMode ? "#2e2e2e" : "#f1f1f1",
                  borderRadius: "3px",
                  marginTop: "1.5rem",
                },
                "&::-webkit-scrollbar-thumb": {
                  background: darkMode ? "#555" : "#888",
                  borderRadius: "3px",
                },
                "&::-webkit-scrollbar-thumb:hover": {
                  background: darkMode ? "#777" : "#555",
                },
              }}
            >
              <Box
                sx={{
                  height: "100px",
                  display: "flex",
                  flexDirection: "column",
                  mt: 3,
                }}
              >
                <TextField
                  label="Remark"
                  variant="outlined"
                  fullWidth
                  multiline
                  rows={6}
                  required
                  value={formData.closureRemark}
                  onChange={(e) => {
                    handleChange("closureRemark", e.target.value);
                    if (validationErrors.closureRemark) {
                      setValidationErrors((prev) => ({
                        ...prev,
                        closureRemark: null,
                      }));
                    }
                  }}
                  error={!!validationErrors.closureRemark}
                  helperText={validationErrors.closureRemark}
                  InputLabelProps={{ shrink: true }}
                  InputProps={{ sx: { color: textColor } }}
                  sx={{ ...textFieldStyle, mb: 2, flex: 1 }}
                />

                <Box sx={{ textAlign: "center", mt: "auto" }}>
                  <Button
                    variant="contained"
                    onClick={handleSubmit}
                    disabled={loading}
                    sx={{
                      backgroundColor: "rgb(18,166,95,0.8)",
                      color: "#fff",
                      px: 3,
                      py: 1,
                      fontSize: "0.875rem",
                      fontWeight: 500,
                      minWidth: 100,
                      textTransform: "none",
                    }}
                  >
                    {loading ? (
                      <CircularProgress size={20} color="inherit" />
                    ) : (
                      "Submit"
                    )}
                  </Button>
                </Box>
              </Box>
            </Box>
          </Grid>
        </Grid>
      </Paper>
    </>
  );
};

export default CaseClosureDetails;
