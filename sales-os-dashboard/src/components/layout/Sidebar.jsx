import { useState } from 'react';
import { NavLink } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import {
  LayoutDashboard, Users, GitBranch, Search, PhoneCall, SendHorizontal,
  ClipboardList, Radio, Activity, BarChart3, Settings, ChevronLeft, PanelRightClose,
} from 'lucide-react';

const menuItems = [
  { path: '/', label: 'Dashboard', icon: LayoutDashboard },
  { path: '/leads', label: 'Leads', icon: Users },
  { path: '/pipeline', label: 'Pipeline', icon: GitBranch },
  { path: '/ai-research', label: 'AI Research', icon: Search },
  { path: '/call-intelligence', label: 'Call Intelligence', icon: PhoneCall },
  { path: '/follow-ups', label: 'Follow-ups', icon: SendHorizontal },
  { path: '/activity-log', label: 'Activity Logs', icon: ClipboardList },
  { path: '/event-monitor', label: 'Event Monitor', icon: Radio },
  { path: '/system-health', label: 'System Health', icon: Activity },
  { path: '/analytics', label: 'Analytics', icon: BarChart3 },
  { path: '/settings', label: 'Settings', icon: Settings },
];

export default function Sidebar({ collapsed, onToggle }) {
  return (
    <motion.aside
      animate={{ width: collapsed ? 72 : 256 }}
      className="h-screen bg-surface/90 backdrop-blur-xl border-r border-white/5 flex flex-col flex-shrink-0 overflow-hidden"
    >
      {/* Logo */}
      <div className="flex items-center gap-3 px-4 h-16 border-b border-white/5 flex-shrink-0">
        <div className="w-8 h-8 rounded-lg bg-primary flex items-center justify-center flex-shrink-0">
          <span className="text-white font-bold text-sm">S</span>
        </div>
        <AnimatePresence>
          {!collapsed && (
            <motion.span initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="text-white font-semibold text-sm whitespace-nowrap">
              Sales OS
            </motion.span>
          )}
        </AnimatePresence>
      </div>

      {/* Nav */}
      <nav className="flex-1 overflow-y-auto py-4 px-2 space-y-1">
        {menuItems.map(item => (
          <NavLink
            key={item.path}
            to={item.path}
            end={item.path === '/'}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2.5 rounded-lg transition-colors ${
                isActive ? 'bg-primary/20 text-primary-300' : 'text-gray-400 hover:text-white hover:bg-white/5'
              }`
            }
          >
            <item.icon size={20} className="flex-shrink-0" />
            <AnimatePresence>
              {!collapsed && (
                <motion.span initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="text-sm whitespace-nowrap">
                  {item.label}
                </motion.span>
              )}
            </AnimatePresence>
          </NavLink>
        ))}
      </nav>

      {/* Collapse button */}
      <button onClick={onToggle} className="flex items-center justify-center h-12 border-t border-white/5 text-gray-500 hover:text-white transition-colors">
        {collapsed ? <PanelRightClose size={18} /> : <ChevronLeft size={18} />}
      </button>
    </motion.aside>
  );
}
