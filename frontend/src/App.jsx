import React, { useEffect, useState } from "react";
import { Activity, Building2, CalendarDays, Plus, Search, Users } from "lucide-react";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

export default function App() {
  const [tenants, setTenants] = useState([]);
  const [tenantId, setTenantId] = useState("tenant-a");
  const [patients, setPatients] = useState([]);
  const [query, setQuery] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ full_name: "", date_of_birth: "", status: "Active" });

  useEffect(() => {
    fetch(`${API_URL}/tenants/`).then((response) => response.json()).then(setTenants).catch(() => setTenants([]));
  }, []);

  useEffect(() => {
    fetch(`${API_URL}/patients/`, { headers: { "X-Tenant": tenantId } })
      .then((response) => response.json())
      .then((data) => setPatients(Array.isArray(data) ? data : []))
      .catch(() => setPatients([]));
  }, [tenantId]);

  const selectedTenant = tenants.find((tenant) => tenant.id === tenantId);
  const filteredPatients = patients.filter((patient) =>
    patient.full_name.toLowerCase().includes(query.toLowerCase())
  );

  async function addPatient(event) {
    event.preventDefault();
    const response = await fetch(`${API_URL}/patients/`, {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-Tenant": tenantId },
      body: JSON.stringify(form),
    });
    if (response.ok) {
      setForm({ full_name: "", date_of_birth: "", status: "Active" });
      setShowForm(false);
      const refreshed = await fetch(`${API_URL}/patients/`, { headers: { "X-Tenant": tenantId } });
      setPatients(await refreshed.json());
    }
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand"><Activity size={22} /> <strong>CareTenant</strong></div>
        <nav>
          <button className="nav-item active"><Users size={18} /> Patients</button>
        </nav>
        <div className="tenant-select-wrap">
          <label>Organization</label>
          <select value={tenantId} onChange={(event) => setTenantId(event.target.value)}>
            {(tenants.length ? tenants : [{ id: "tenant-a", name: "Tenant A Hospital" }, { id: "tenant-b", name: "Tenant B Hospital" }]).map((tenant) => (
              <option key={tenant.id} value={tenant.id}>{tenant.name}</option>
            ))}
          </select>
        </div>
      </aside>

      <main>
        <header className="topbar">
          <div>
            <p className="eyebrow">Patient registry</p>
            <h1>{selectedTenant?.name || (tenantId === "tenant-a" ? "Tenant A Hospital" : "Tenant B Hospital")}</h1>
          </div>
          <button className="primary-button" onClick={() => setShowForm(true)}><Plus size={17} /> Add patient</button>
        </header>

        <section className="stats" aria-label="Patient summary">
          <div className="stat"><Users size={20} /><div><span>Total patients</span><strong>{patients.length}</strong></div></div>
          <div className="stat"><Building2 size={20} /><div><span>Organization</span><strong>{tenantId.replace("tenant-", "Tenant ").toUpperCase()}</strong></div></div>
        </section>

        <section className="patient-panel">
          <div className="panel-toolbar">
            <h2>Patients</h2>
            <label className="search"><Search size={16} /><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search patients" /></label>
          </div>

          <div className="table-wrap">
            <table>
              <thead><tr><th>Patient</th><th>Date of birth</th><th>Status</th></tr></thead>
              <tbody>
                {filteredPatients.map((patient) => (
                  <tr key={patient.id}>
                    <td><span className="avatar">{patient.full_name.split(" ").map((word) => word[0]).join("").slice(0, 2)}</span><strong>{patient.full_name}</strong></td>
                    <td><CalendarDays size={15} /> {patient.date_of_birth}</td>
                    <td><span className="status">{patient.status}</span></td>
                  </tr>
                ))}
                {!filteredPatients.length && <tr><td colSpan="3" className="empty">No patients found in this organization.</td></tr>}
              </tbody>
            </table>
          </div>
        </section>
      </main>

      {showForm && <div className="modal-backdrop" onMouseDown={() => setShowForm(false)}>
        <form className="modal" onSubmit={addPatient} onMouseDown={(event) => event.stopPropagation()}>
          <h2>Add patient</h2>
          <label>Full name<input required value={form.full_name} onChange={(event) => setForm({ ...form, full_name: event.target.value })} /></label>
          <label>Date of birth<input required type="date" value={form.date_of_birth} onChange={(event) => setForm({ ...form, date_of_birth: event.target.value })} /></label>
          <label>Status<select value={form.status} onChange={(event) => setForm({ ...form, status: event.target.value })}><option>Active</option><option>Inactive</option></select></label>
          <div className="modal-actions"><button type="button" className="secondary-button" onClick={() => setShowForm(false)}>Cancel</button><button className="primary-button">Add patient</button></div>
        </form>
      </div>}
    </div>
  );
}
