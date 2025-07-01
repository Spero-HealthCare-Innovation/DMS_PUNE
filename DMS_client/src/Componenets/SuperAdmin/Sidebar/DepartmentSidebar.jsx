import { useState } from "react";
import {
  Drawer,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Box,
  Grid,
  Typography,
} from "@mui/material";
import AccountCircleIcon from "@mui/icons-material/AccountCircle";
import ArrowDropDownIcon from "@mui/icons-material/ArrowDropDown";
import ArrowDropUpIcon from "@mui/icons-material/ArrowDropUp";
import LockIcon from "@mui/icons-material/Lock";
import { useNavigate } from "react-router-dom";
import AddBoxIcon from "@mui/icons-material/AddBox";
import AddCircleOutlineOutlinedIcon from "@mui/icons-material/AddCircleOutlineOutlined";
import TextSnippetOutlinedIcon from "@mui/icons-material/TextSnippetOutlined";

const screenConfig = {
  "System User": {
    icon: <AccountCircleIcon />,
    screens: [
      { id: 1, text: "Add Department", path: "/add-department" },
      { id: 2, text: "Add Group", path: "/add-group" },
      { id: 3, text: "Add Employee", path: "/add-employee" },
    ],
  },
  "Register Sop": {
    icon: <AddBoxIcon />,
    screens: [],
  },
  Responder: {
    icon: <AddCircleOutlineOutlinedIcon />,
    screens: [],
  },
  // "Closure Report": {
  //   icon: <TextSnippetOutlinedIcon />,
  //   screens: [],
  // },

  "Reports": {
    icon: <TextSnippetOutlinedIcon />,
    screens: [
      { id: 1, text: "Closure Report", path: "/Closure Report" },
      { id: 2, text: "Incident Report", path: "/Incident Report" },
    ],
  },
  Permission: {
    icon: <LockIcon />,
    screens: [
      { id: 4, text: "Manage Roles", path: "/roles" },
      { id: 5, text: "Access Control", path: "/access-control" },
    ],
  },
};

const Departmentsidebar = ({ darkMode }) => {
  const [open, setOpen] = useState(false);
  const [dropdowns, setDropdowns] = useState({});
  const navigate = useNavigate();

  const toggleDropdown = (key) => {
    setDropdowns((prev) => ({
      ...prev,
      [key]: !prev[key],
    }));
  };

  return (
    <Grid container>
      <Grid item>
        <Drawer
          variant="permanent"
          onMouseEnter={() => setOpen(true)}
          onMouseLeave={() => {
            setOpen(false);
            setDropdowns({});
          }}
          sx={{
            width: open ? 200 : 60,
            "& .MuiDrawer-paper": {
              width: open ? 200 : 45,
              position: "absolute",
              top: "50%",
              transform: "translateY(-50%)",
              background: darkMode
                ? open
                  ? "linear-gradient(to bottom, #5FC8EC,rgb(19, 26, 28))" // top to bottom gradient when open
                  : "linear-gradient(to bottom, #5FC8EC,rgb(19, 26, 28))" // solid background when closed
                : open
                  ? "linear-gradient(to bottom, #5FC8EC,rgb(18, 24, 26))" // light gradient when open in light mode
                  : "radial-gradient(6035.71% 72.44% at 0% 50%, #5FC8EC 0%, #5FC8EC 100%)",

              borderRadius: "30px",
              // transition: "width 0.5s ease-in-out",
              display: "flex",
              alignItems: open ? "flex-start" : "center",
              justifyContent: "center",
              overflow: "hidden",
              height: "auto",
              // maxHeight: "90vh",
              svg: {
                fill: "#fff",
              },
              pt: 2,
              pb: 2,
              marginLeft: "0.5em",
              fontSize: "18px",
              color: "white",
              boxShadow: "0 0 10px rgba(0, 0, 0, 0.1)",
              alignContent: "left",
              "&:hover": {
                background: open
                  ? "linear-gradient(to bottom, #5FC8EC, #2F4D54)"
                  : "radial-gradient(6035.71% 72.44% at 0% 50%, #5FC8EC 0%, #5FC8EC 100%)",
              },
            },
          }}
        >
          <Box sx={{ width: "100%", overflow: "hidden", alignContent: "left" }}>
            <List>
              {Object.entries(screenConfig).map(
                ([sectionName, { icon, screens }]) => {
                  const hasSubmenus = screens && screens.length > 0;

                  return (
                    <Box key={sectionName} sx={{ width: "100%" }}>
                      <ListItemButton
                        onClick={() =>
                          hasSubmenus
                            ? toggleDropdown(sectionName)
                            : navigate(sectionName)
                        }
                        sx={{
                          flexDirection: open ? "row" : "column",
                          justifyContent: "left",
                          py: 1,
                          gap: 1,
                          color: 'white'
                        }}
                      >
                        <ListItemIcon sx={{ minWidth: 0, color: 'white' }}>{icon}</ListItemIcon>

                        {open && (
                          <Box
                            sx={{
                              display: "flex",
                              alignItems: "center",
                              gap: 0.5,
                            }}
                          >
                            <Typography variant="caption">
                              {sectionName}
                            </Typography>
                            {hasSubmenus &&
                              (dropdowns[sectionName] ? (
                                <ArrowDropUpIcon fontSize="small" sx={{ color: "white" }} />
                              ) : (
                                <ArrowDropDownIcon fontSize="small" sx={{ color: "white" }} />
                              ))}
                          </Box>
                        )}
                      </ListItemButton>

                      {open && dropdowns[sectionName] && hasSubmenus && (
                        <Box sx={{ mt: 1, pl: 3 }}>
                          {screens.map((screen) => (
                            <ListItemButton
                              key={screen.id}
                              onClick={() => navigate(screen.path)}
                              sx={{ py: 0.5 }}
                            >
                              <ListItemText
                                primary={screen.text}
                                primaryTypographyProps={{ fontSize: 12 }}
                              />
                            </ListItemButton>
                          ))}
                        </Box>
                      )}
                    </Box>
                  );
                }
              )}
            </List>
          </Box>
        </Drawer>
      </Grid>
    </Grid>
  );
};

export default Departmentsidebar;
