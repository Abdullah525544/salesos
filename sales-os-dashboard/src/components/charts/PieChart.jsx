import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, Legend } from 'recharts';

const CustomTooltip = ({ active, payload }) => {
  if (!active || !payload?.length) return null;
  const d = payload[0];
  return (
    <div className="glass-card !p-3 !rounded-lg text-sm">
      <p className="text-white font-medium">{d.name}</p>
      <p className="text-gray-400 mt-1">{d.value} leads ({((d.value / 847) * 100).toFixed(1)}%)</p>
    </div>
  );
};

export default function CustomPieChart({ data }) {
  return (
    <ResponsiveContainer width="100%" height={280}>
      <PieChart>
        <Pie data={data} cx="50%" cy="50%" innerRadius={60} outerRadius={100} paddingAngle={4} dataKey="value">
          {data.map((entry, i) => (
            <Cell key={i} fill={entry.fill} stroke="transparent" />
          ))}
        </Pie>
        <Tooltip content={<CustomTooltip />} />
        <Legend wrapperStyle={{ fontSize: 12, color: '#9CA3AF' }} />
      </PieChart>
    </ResponsiveContainer>
  );
}
