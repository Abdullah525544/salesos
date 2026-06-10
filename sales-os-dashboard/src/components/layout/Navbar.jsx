import { Search, Bell, User } from 'lucide-react';
import { useState } from 'react';

export default function Navbar() {
  const [showNotifications, setShowNotifications] = useState(false);

  return (
    <header className="h-16 border-b border-white/5 flex items-center justify-between px-6 bg-surface/50 backdrop-blur-xl">
      {/* Search */}
      <div className="relative max-w-md w-full">
        <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500" />
        <input
          type="text"
          placeholder="Search leads, companies, events..."
          className="w-full bg-surface-light border border-gray-600 rounded-lg pl-10 pr-4 py-2 text-sm text-white placeholder-gray-400 focus:outline-none focus:border-primary transition-colors"
        />
      </div>

      {/* Right actions */}
      <div className="flex items-center gap-4">
        {/* Notifications */}
        <div className="relative">
          <button onClick={() => setShowNotifications(!showNotifications)} className="relative p-2 rounded-lg hover:bg-white/5 transition-colors">
            <Bell size={20} className="text-gray-400" />
            <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-red-500 rounded-full" />
          </button>
          {showNotifications && (
            <div className="absolute right-0 top-full mt-2 w-72 glass-card p-3 z-50">
              <p className="text-xs text-gray-400 mb-2">Notifications</p>
              <div className="space-y-2">
                <p className="text-sm text-gray-300">New lead created: Harbor Dental Group</p>
                <p className="text-sm text-gray-300">Research completed for City Dental Care</p>
                <p className="text-sm text-gray-300">Call scheduled with Dr. Kim at 2PM</p>
              </div>
            </div>
          )}
        </div>

        {/* Profile */}
        <div className="flex items-center gap-3 pl-4 border-l border-white/5">
          <div className="text-right">
            <p className="text-sm font-medium text-white">Dr. Admin</p>
            <p className="text-xs text-gray-400">Sales OS Manager</p>
          </div>
          <div className="w-9 h-9 rounded-full bg-primary/20 flex items-center justify-center">
            <User size={18} className="text-primary-300" />
          </div>
        </div>
      </div>
    </header>
  );
}
