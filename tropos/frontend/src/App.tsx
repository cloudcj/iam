import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import RegionsPage from './pages/infrastructure/RegionsPage'
import RacksPage from './pages/infrastructure/RacksPage'
import DevicesPage from './pages/assets/DevicesPage'
import ServersPage from './pages/assets/ServersPage'
import SwitchesPage from './pages/assets/SwitchesPage'
import AppliancesPage from './pages/assets/AppliancesPage'
import UsersPage from './pages/users/UsersPage'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Navigate to="/dashboard" replace />} />
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="infrastructure/regions" element={<RegionsPage />} />
          <Route path="infrastructure/racks" element={<RacksPage />} />
          <Route path="assets/devices" element={<DevicesPage />} />
          <Route path="assets/servers" element={<ServersPage />} />
          <Route path="assets/switches" element={<SwitchesPage />} />
          <Route path="assets/appliances" element={<AppliancesPage />} />
          <Route path="users" element={<UsersPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}
