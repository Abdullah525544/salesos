export const kpiData = {
  totalLeads: { value: 2483, change: 12.5 },
  activeLeads: { value: 847, change: 8.2 },
  hotLeads: { value: 163, change: -3.1 },
  callsMade: { value: 1429, change: 18.7 },
  followupsSent: { value: 672, change: 5.4 },
  systemHealth: { value: 97, change: 1.2 },
};

export const pipelineFunnel = [
  { name: 'New', value: 847, fill: '#6B7280' },
  { name: 'Researching', value: 512, fill: '#3B82F6' },
  { name: 'Contacted', value: 328, fill: '#8B5CF6' },
  { name: 'Qualified', value: 163, fill: '#4F46E5' },
  { name: 'Converted', value: 71, fill: '#10B981' },
];

export const dailyActivity = [
  { day: 'Mon', leads: 24, calls: 38, followups: 12 },
  { day: 'Tue', leads: 31, calls: 45, followups: 18 },
  { day: 'Wed', leads: 28, calls: 52, followups: 15 },
  { day: 'Thu', leads: 35, calls: 41, followups: 22 },
  { day: 'Fri', leads: 42, calls: 63, followups: 28 },
  { day: 'Sat', leads: 18, calls: 22, followups: 8 },
  { day: 'Sun', leads: 12, calls: 15, followups: 5 },
];

export const recentEvents = [
  { id: 'evt_001', type: 'lead.created', lead: 'BrightStar Dental', time: '2m ago', icon: 'UserPlus', color: 'green' },
  { id: 'evt_002', type: 'research.completed', lead: 'SmileCare Clinic', time: '5m ago', icon: 'Search', color: 'blue' },
  { id: 'evt_003', type: 'call.completed', lead: 'Elite Dentistry', time: '8m ago', icon: 'Phone', color: 'indigo' },
  { id: 'evt_004', type: 'lead.qualified', lead: 'Prime Dental Group', time: '12m ago', icon: 'Award', color: 'emerald' },
  { id: 'evt_005', type: 'follow_up.sent', lead: 'City Dental Care', time: '15m ago', icon: 'Send', color: 'purple' },
  { id: 'evt_006', type: 'lead.created', lead: 'New Horizon Dental', time: '18m ago', icon: 'UserPlus', color: 'green' },
  { id: 'evt_007', type: 'call.completed', lead: 'Golden Gate Dental', time: '22m ago', icon: 'Phone', color: 'indigo' },
  { id: 'evt_008', type: 'research.completed', lead: 'Pacific Dental', time: '28m ago', icon: 'Search', color: 'blue' },
];

export const leads = [
  { id: 1, name: 'Dr. Sarah Chen', company: 'BrightStar Dental', email: 'sarah@brightstar.com', phone: '+1 (415) 555-0101', score: 92, status: 'Hot', lastActivity: '2m ago', city: 'San Francisco', source: 'Google Places', industry: 'Dentist', rating: 4.8 },
  { id: 2, name: 'Dr. Michael Torres', company: 'SmileCare Clinic', email: 'michael@smilecare.com', phone: '+1 (415) 555-0102', score: 78, status: 'Warm', lastActivity: '15m ago', city: 'Oakland', source: 'Referral', industry: 'Dentist', rating: 4.5 },
  { id: 3, name: 'Dr. Emily Watson', company: 'Elite Dentistry', email: 'emily@elite-dent.com', phone: '+1 (510) 555-0103', score: 65, status: 'Warm', lastActivity: '1h ago', city: 'San Jose', source: 'LinkedIn', industry: 'Dentist', rating: 4.2 },
  { id: 4, name: 'Dr. James Rodriguez', company: 'Prime Dental Group', email: 'james@primedental.com', phone: '+1 (650) 555-0104', score: 88, status: 'Hot', lastActivity: '30m ago', city: 'Palo Alto', source: 'Google Places', industry: 'Dental Group', rating: 4.9 },
  { id: 5, name: 'Dr. Lisa Park', company: 'City Dental Care', email: 'lisa@citydental.com', phone: '+1 (408) 555-0105', score: 45, status: 'Cold', lastActivity: '3h ago', city: 'Sunnyvale', source: 'Website', industry: 'Dentist', rating: 3.8 },
  { id: 6, name: 'Dr. Robert Kim', company: 'New Horizon Dental', email: 'robert@nhdental.com', phone: '+1 (925) 555-0106', score: 81, status: 'Hot', lastActivity: '45m ago', city: 'Walnut Creek', source: 'Google Places', industry: 'Dentist', rating: 4.6 },
  { id: 7, name: 'Dr. Amanda Foster', company: 'Golden Gate Dental', email: 'amanda@goldengate.com', phone: '+1 (415) 555-0107', score: 55, status: 'Warm', lastActivity: '2h ago', city: 'San Francisco', source: 'Referral', industry: 'Dentist', rating: 4.0 },
  { id: 8, name: 'Dr. David Nguyen', company: 'Pacific Dental', email: 'david@pacificdental.com', phone: '+1 (510) 555-0108', score: 72, status: 'Warm', lastActivity: '1.5h ago', city: 'Berkeley', source: 'Conference', industry: 'Dentist', rating: 4.3 },
  { id: 9, name: 'Dr. Rachel Thompson', company: 'Harbor Dental Group', email: 'rachel@harbordental.com', phone: '+1 (415) 555-0109', score: 35, status: 'Cold', lastActivity: '5h ago', city: 'Sausalito', source: 'Website', industry: 'Dental Group', rating: 3.5 },
  { id: 10, name: 'Dr. Kevin Patel', company: 'Valley Smile Dental', email: 'kevin@valleysmile.com', phone: '+1 (669) 555-0110', score: 95, status: 'Hot', lastActivity: '10m ago', city: 'Fremont', source: 'Google Places', industry: 'Dentist', rating: 5.0 },
];

export const leadDetail = {
  id: 1,
  name: 'Dr. Sarah Chen',
  company: 'BrightStar Dental',
  email: 'sarah@brightstar.com',
  phone: '+1 (415) 555-0101',
  website: 'https://brightstardental.com',
  address: '123 Market St, San Francisco, CA 94105',
  city: 'San Francisco',
  country: 'US',
  score: 92,
  status: 'Hot',
  source: 'Google Places',
  industry: 'Dentist',
  rating: 4.8,
  reviews: 127,
  created_at: '2026-06-01',
  pipeline_stage: 'qualified',
  aiInsights: {
    sentiment: 8.5,
    suggestedAction: 'Schedule demo call',
    nextFollowUp: '2026-06-09T10:00:00Z',
    painPoints: ['Outdated patient booking system', 'High no-show rate', 'Manual insurance verification'],
    opportunities: ['AI scheduling can reduce no-shows by 40%', 'Automated insurance checks save 12h/week'],
    scoreExplanation: 'High Google rating (4.8), active online presence, decision-maker title confirmed, budget available per LinkedIn profile.',
    recommendations: ['Send ROI calculator', 'Reference similar dental practice case study', 'Offer 14-day free trial'],
  },
  activity: [
    { type: 'Lead Created', date: '2026-06-01', detail: 'Lead imported from Google Places' },
    { type: 'Research Completed', date: '2026-06-02', detail: 'AI research completed — 3 pain points identified' },
    { type: 'Call Scheduled', date: '2026-06-04', detail: 'Discovery call scheduled via email' },
    { type: 'Call Completed', date: '2026-06-04', detail: '35min discovery call — positive sentiment' },
    { type: 'Qualified', date: '2026-06-05', detail: 'BANT criteria met — moving to proposal' },
  ],
};

export const callIntelligence = [
  { id: 1, lead: 'BrightStar Dental', date: '2026-06-04', duration: '35:12', sentiment: 8.5, bant: { budget: true, authority: true, need: true, timeline: true }, objections: ['Pricing concerns', 'Integration complexity'], transcript: 'Dr. Chen: We\'ve been looking for a solution to reduce no-shows...\nAgent: Our AI system can help with that...\nDr. Chen: What about integration with our existing PMS?\nAgent: We support all major PMS APIs...', recommendations: ['Send pricing comparison', 'Offer integration whitepaper', 'Schedule technical demo'] },
  { id: 2, lead: 'SmileCare Clinic', date: '2026-06-03', duration: '28:45', sentiment: 7.2, bant: { budget: true, authority: false, need: true, timeline: false }, objections: ['Need board approval'], transcript: 'Dr. Torres: The concept is interesting.\nAgent: Let me show you how we helped similar clinics...', recommendations: ['Send case studies', 'Prepare board presentation package'] },
  { id: 3, lead: 'Elite Dentistry', date: '2026-06-02', duration: '42:10', sentiment: 9.0, bant: { budget: true, authority: true, need: true, timeline: true }, objections: ['None'], transcript: 'Dr. Watson: When can we start?\nAgent: We can have you onboarded within a week...', recommendations: ['Send contract', 'Assign onboarding specialist'] },
];

export const analyticsData = {
  conversionRate: [
    { month: 'Jan', rate: 12 }, { month: 'Feb', rate: 15 }, { month: 'Mar', rate: 18 },
    { month: 'Apr', rate: 22 }, { month: 'May', rate: 25 }, { month: 'Jun', rate: 28 },
  ],
  qualityDistribution: [
    { name: 'Hot', value: 163, fill: '#EF4444' },
    { name: 'Warm', value: 412, fill: '#F59E0B' },
    { name: 'Cold', value: 272, fill: '#6B7280' },
  ],
  responseTime: [
    { day: 'Mon', hours: 4.2 }, { day: 'Tue', hours: 3.8 }, { day: 'Wed', hours: 5.1 },
    { day: 'Thu', hours: 3.5 }, { day: 'Fri', hours: 4.8 }, { day: 'Sat', hours: 6.2 },
    { day: 'Sun', hours: 7.5 },
  ],
  aiEfficiency: [
    { metric: 'Lead Scoring Accuracy', value: 94 },
    { metric: 'Sentiment Detection', value: 89 },
    { metric: 'Pain Point Identification', value: 92 },
    { metric: 'Recommendation Relevance', value: 86 },
  ],
  pipelinePerformance: [
    { stage: 'New', value: 847, target: 1000 },
    { stage: 'Researching', value: 512, target: 750 },
    { stage: 'Contacted', value: 328, target: 500 },
    { stage: 'Qualified', value: 163, target: 250 },
    { stage: 'Converted', value: 71, target: 100 },
  ],
};

export const systemHealthData = {
  eventBus: { status: 'healthy', latency: '12ms', uptime: '99.97%' },
  orchestrator: { status: 'healthy', latency: '45ms', uptime: '99.95%' },
  apiLatency: { current: '187ms', avg: '165ms', p95: '320ms' },
  costPerLead: { current: '$2.47', trend: 'decreasing', change: 8 },
  errorRate: { current: '0.3%', threshold: '1.0%', status: 'good' },
  queue: { pending: 23, processing: 5, failed: 1, depth: 29 },
};

export const activityLogs = [
  { id: 'act_001', type: 'lead.created', lead: 'BrightStar Dental', user: 'System', timestamp: '2026-06-08T14:32:00Z', detail: 'Lead auto-created from Google Places API' },
  { id: 'act_002', type: 'research.completed', lead: 'SmileCare Clinic', user: 'AI Research Engine', timestamp: '2026-06-08T14:28:00Z', detail: 'Research completed — found 3 pain points, 2 opportunities' },
  { id: 'act_003', type: 'call.completed', lead: 'Elite Dentistry', user: 'Agent Smith', timestamp: '2026-06-08T14:15:00Z', detail: '35min discovery call — sentiment: 8.5/10' },
  { id: 'act_004', type: 'lead.qualified', lead: 'Prime Dental Group', user: 'AI Scoring', timestamp: '2026-06-08T13:55:00Z', detail: 'Lead scored 88 — automatically qualified' },
  { id: 'act_005', type: 'follow_up.sent', lead: 'City Dental Care', user: 'Automation', timestamp: '2026-06-08T13:30:00Z', detail: 'Follow-up email sent — ROI calculator link' },
  { id: 'act_006', type: 'lead.updated', lead: 'New Horizon Dental', user: 'Dr. Robert Kim', timestamp: '2026-06-08T13:22:00Z', detail: 'Contact information updated' },
  { id: 'act_007', type: 'call.scheduled', lead: 'Golden Gate Dental', user: 'System', timestamp: '2026-06-08T13:00:00Z', detail: 'Call scheduled for Jun 10 at 2:00 PM' },
  { id: 'act_008', type: 'lead.created', lead: 'Harbor Dental Group', user: 'System', timestamp: '2026-06-08T12:45:00Z', detail: 'Lead imported from LinkedIn Ads' },
];

export const followups = [
  { id: 'fu_001', lead: 'BrightStar Dental', type: 'Email — ROI Calculator', due: '2026-06-09T10:00:00Z', status: 'pending', priority: 'high' },
  { id: 'fu_002', lead: 'Elite Dentistry', type: 'Call — Technical Demo', due: '2026-06-09T14:00:00Z', status: 'scheduled', priority: 'high' },
  { id: 'fu_003', lead: 'Pacific Dental', type: 'Email — Case Studies', due: '2026-06-10T09:00:00Z', status: 'pending', priority: 'medium' },
  { id: 'fu_004', lead: 'SmileCare Clinic', type: 'Call — Board Presentation Prep', due: '2026-06-11T11:00:00Z', status: 'draft', priority: 'medium' },
  { id: 'fu_005', lead: 'Prime Dental Group', type: 'Email — Contract Review', due: '2026-06-08T16:00:00Z', status: 'completed', priority: 'high' },
  { id: 'fu_006', lead: 'Valley Smile Dental', type: 'Call — Welcome Call', due: '2026-06-12T13:00:00Z', status: 'pending', priority: 'low' },
];

export const aiResearch = [
  { id: 'res_001', lead: 'BrightStar Dental', status: 'completed', summary: 'High-intent prospect. Strong online presence, 4.8 stars, 127 reviews. Recently expanded office.', painPoints: ['Outdated booking system', 'High no-show rate'], score: 92, completedAt: '2026-06-02' },
  { id: 'res_002', lead: 'SmileCare Clinic', status: 'completed', summary: 'Growing practice with 3 locations. Active social media. Moderate online presence.', painPoints: ['Manual insurance verification', 'Staff scheduling challenges'], score: 78, completedAt: '2026-06-03' },
  { id: 'res_003', lead: 'Elite Dentistry', status: 'completed', summary: 'Premium practice in affluent area. Very active online. Recent technology investment signals budget availability.', painPoints: ['Patient retention', 'Competitive pressure'], score: 65, completedAt: '2026-06-03' },
  { id: 'res_004', lead: 'City Dental Care', status: 'in_progress', summary: '', painPoints: [], score: 0, completedAt: null },
  { id: 'res_005', lead: 'Harbor Dental Group', status: 'pending', summary: '', painPoints: [], score: 0, completedAt: null },
];

export const kanbanStages = [
  { id: 'new', title: 'New', items: [
    { id: 'k_1', title: 'Harbor Dental Group', score: 35, priority: 'low', assignee: 'Unassigned' },
    { id: 'k_2', title: 'Bay Area Dental', score: 42, priority: 'medium', assignee: 'Alice' },
    { id: 'k_3', title: 'Sunset Dentistry', score: 28, priority: 'low', assignee: 'Unassigned' },
  ]},
  { id: 'researching', title: 'Researching', items: [
    { id: 'k_4', title: 'City Dental Care', score: 45, priority: 'medium', assignee: 'Bob' },
    { id: 'k_5', title: 'Pacific Dental', score: 72, priority: 'high', assignee: 'Alice' },
  ]},
  { id: 'contacted', title: 'Contacted', items: [
    { id: 'k_6', title: 'SmileCare Clinic', score: 78, priority: 'high', assignee: 'Bob' },
    { id: 'k_7', title: 'Golden Gate Dental', score: 55, priority: 'medium', assignee: 'Alice' },
    { id: 'k_8', title: 'Elite Dentistry', score: 65, priority: 'medium', assignee: 'Bob' },
  ]},
  { id: 'qualified', title: 'Qualified', items: [
    { id: 'k_9', title: 'BrightStar Dental', score: 92, priority: 'high', assignee: 'Alice' },
    { id: 'k_10', title: 'Prime Dental Group', score: 88, priority: 'high', assignee: 'Bob' },
  ]},
  { id: 'converted', title: 'Converted', items: [
    { id: 'k_11', title: 'New Horizon Dental', score: 81, priority: 'high', assignee: 'Alice' },
    { id: 'k_12', title: 'Valley Smile Dental', score: 95, priority: 'high', assignee: 'Bob' },
  ]},
];
