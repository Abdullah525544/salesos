import { Save, Settings as SettingsIcon, Bell, Shield, Sliders, Database } from 'lucide-react';

const sections = [
  {
    title: 'General', icon: SettingsIcon, fields: [
      { label: 'Organization Name', value: 'Dograh Sales', type: 'text' },
      { label: 'Default Pipeline Stage', value: 'New', type: 'select', options: ['New', 'Researching', 'Contacted', 'Qualified'] },
      { label: 'Leads per Page', value: '25', type: 'select', options: ['10', '25', '50', '100'] },
    ],
  },
  {
    title: 'Notifications', icon: Bell, fields: [
      { label: 'Email Alerts', value: 'Enabled', type: 'toggle' },
      { label: 'Slack Integration', value: 'Disabled', type: 'toggle' },
      { label: 'Daily Digest', value: 'Enabled', type: 'toggle' },
    ],
  },
  {
    title: 'AI Configuration', icon: Sliders, fields: [
      { label: 'Auto-Research New Leads', value: 'Enabled', type: 'toggle' },
      { label: 'Auto-Qualification Threshold', value: '75', type: 'text' },
      { label: 'Sentiment Sensitivity', value: 'Medium', type: 'select', options: ['Low', 'Medium', 'High'] },
    ],
  },
  {
    title: 'Security', icon: Shield, fields: [
      { label: 'Two-Factor Auth', value: 'Disabled', type: 'toggle' },
      { label: 'API Key Rotation', value: '90 days', type: 'select', options: ['30 days', '60 days', '90 days'] },
    ],
  },
  {
    title: 'Data Management', icon: Database, fields: [
      { label: 'Retention Period', value: '12 months', type: 'select', options: ['3 months', '6 months', '12 months', '24 months'] },
      { label: 'Export Format', value: 'CSV', type: 'select', options: ['CSV', 'JSON', 'Excel'] },
    ],
  },
];

export default function Settings() {
  return (
    <div className="space-y-6 max-w-3xl">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Settings</h1>
          <p className="text-sm text-gray-400 mt-1">Configure your Sales OS instance</p>
        </div>
        <button className="btn-primary"><Save size={16} className="mr-2 inline" /> Save Changes</button>
      </div>

      {sections.map(section => (
        <div key={section.title} className="glass-card">
          <div className="flex items-center gap-2 mb-4">
            <section.icon size={18} className="text-primary-300" />
            <h3 className="text-sm font-semibold text-white">{section.title}</h3>
          </div>
          <div className="space-y-4">
            {section.fields.map(field => (
              <div key={field.label} className="flex items-center justify-between">
                <label className="text-sm text-gray-300">{field.label}</label>
                {field.type === 'toggle' ? (
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input type="checkbox" defaultChecked={field.value === 'Enabled'} className="sr-only peer" />
                    <div className="w-10 h-5 bg-surface-light rounded-full peer peer-checked:bg-primary after:content-[''] after:absolute after:top-0.5 after:left-0.5 after:bg-white after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:after:translate-x-5" />
                  </label>
                ) : field.type === 'select' ? (
                  <select defaultValue={field.value} className="input-field w-auto">
                    {field.options.map(o => <option key={o} value={o}>{o}</option>)}
                  </select>
                ) : (
                  <input type="text" defaultValue={field.value} className="input-field w-48" />
                )}
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
