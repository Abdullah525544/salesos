import { Routes, Route, Navigate } from 'react-router-dom';
import MainLayout from './components/layout/MainLayout';
import Dashboard from './pages/Dashboard';
import Leads from './pages/Leads';
import LeadCreate from './pages/LeadCreate';
import LeadDetail from './pages/LeadDetail';
import Pipeline from './pages/Pipeline';
import AIResearch from './pages/AIResearch';
import CallIntelligence from './pages/CallIntelligence';
import FollowUps from './pages/FollowUps';
import ActivityLog from './pages/ActivityLog';
import EventMonitor from './pages/EventMonitor';
import SystemHealth from './pages/SystemHealth';
import Analytics from './pages/Analytics';
import Settings from './pages/Settings';

export default function App() {
  return (
    <Routes>
      <Route element={<MainLayout />}>
        <Route path="/" element={<Dashboard />} />
        <Route path="/leads" element={<Leads />} />
        <Route path="/leads/create" element={<LeadCreate />} />
        <Route path="/leads/:id" element={<LeadDetail />} />
        <Route path="/pipeline" element={<Pipeline />} />
        <Route path="/ai-research" element={<AIResearch />} />
        <Route path="/call-intelligence" element={<CallIntelligence />} />
        <Route path="/follow-ups" element={<FollowUps />} />
        <Route path="/activity-log" element={<ActivityLog />} />
        <Route path="/event-monitor" element={<EventMonitor />} />
        <Route path="/system-health" element={<SystemHealth />} />
        <Route path="/analytics" element={<Analytics />} />
        <Route path="/settings" element={<Settings />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Route>
    </Routes>
  );
}
