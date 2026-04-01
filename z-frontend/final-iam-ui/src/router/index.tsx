import { createBrowserRouter } from 'react-router-dom'
import ProtectedRoute from './ProtectedRoute'
import Layout from '../components/layout/Layout'
import LoginPage from '../pages/LoginPage'
import DashboardPage from '../pages/DashboardPage'
import UsersPage from '../pages/UsersPage'
import DepartmentsPage from '../pages/DepartmentsPage'
import ApprovalPage from '../pages/ApprovalPage'
import ProfilePage from '../pages/ProfilePage'
import AuditLogPage from '../pages/AuditLogPage'
import DevicesPage from '../pages/tropos/assets/DevicesPage'
import RacksPage from '../pages/tropos/infrastructure/RacksPage'
import RegionsPage from '../pages/tropos/infrastructure/RegionsPage'
import TroposDashboardPage from '../pages/tropos/TroposDashboardPage'

export const router = createBrowserRouter([
  { path: '/login', element: <LoginPage /> },
  {
    path: '/',
    element: (
      <ProtectedRoute>
        <Layout />
      </ProtectedRoute>
    ),
    children: [
      { index: true, element: <DashboardPage /> },
      { path: 'users', element: <UsersPage /> },
      { path: 'departments', element: <DepartmentsPage /> },
      { path: 'approvals', element: <ApprovalPage /> },
      { path: 'profile', element: <ProfilePage /> },
      { path: 'audit', element: <AuditLogPage /> },
      
      { path: 'tropos', element: <TroposDashboardPage /> },
      { path: 'tropos/regions', element: <RegionsPage /> },
      { path: 'tropos/racks', element: <RacksPage /> },
      { path: 'tropos/devices', element: <DevicesPage /> },

    ],
  },
])
