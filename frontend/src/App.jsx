import { useEffect, useState } from "react";

const API_BASE = "https://hrms-lite-backend-jonk.onrender.com";

function App() {
  const [employees, setEmployees] = useState([]);
  const [selectedEmp, setSelectedEmp] = useState("");
  const [attendance, setAttendance] = useState([]);
  const [status, setStatus] = useState("Present");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API_BASE}/employees`)
      .then((res) => res.json())
      .then((data) => {
        setEmployees(data);
        setLoading(false);
      });
  }, []);

  const loadAttendance = (empId) => {
    fetch(`${API_BASE}/attendance/${empId}`)
      .then((res) => res.json())
      .then((data) => setAttendance(data));
  };

  const markAttendance = () => {
    if (!selectedEmp) {
      alert("Please select employee");
      return;
    }

    const payload = {
      employee_id: Number(selectedEmp),
      date: new Date().toISOString().split("T")[0],
      status,
    };

    fetch(`${API_BASE}/attendance`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    }).then(() => {
      loadAttendance(selectedEmp);
      alert("Attendance marked");
    });
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>HRMS Lite</h1>

      {!loading && (
        <table border="1" cellPadding="10">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Email</th>
              <th>Department</th>
            </tr>
          </thead>
          <tbody>
            {employees.map((emp) => (
              <tr key={emp.id}>
                <td>{emp.employee_id}</td>
                <td>{emp.full_name}</td>
                <td>{emp.email}</td>
                <td>{emp.department}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      <h2>Attendance</h2>

      <select
        value={selectedEmp}
        onChange={(e) => {
          setSelectedEmp(e.target.value);
          loadAttendance(e.target.value);
        }}
      >
        <option value="">Select Employee</option>
        {employees.map((emp) => (
          <option key={emp.id} value={emp.id}>
            {emp.full_name}
          </option>
        ))}
      </select>

      <select
        value={status}
        onChange={(e) => setStatus(e.target.value)}
      >
        <option value="Present">Present</option>
        <option value="Absent">Absent</option>
      </select>

      <button onClick={markAttendance}>Mark Attendance</button>

      {attendance.length > 0 && (
        <>
          <h3>Attendance History</h3>
          <table border="1">
            <tbody>
              {attendance.map((a) => (
                <tr key={a.id}>
                  <td>{a.date}</td>
                  <td>{a.status}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </>
      )}
    </div>
  );
}

export default App;
