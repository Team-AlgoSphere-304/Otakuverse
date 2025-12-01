import React from 'react';
import { useAuthStore } from '../store/useStore';
import { User as UserIcon, Mail, Shield, Settings } from 'lucide-react';

const Profile: React.FC = () => {
  const { user } = useAuthStore();

  if (!user) return null;

  return (
    <div className="max-w-2xl mx-auto space-y-8">
      <h1 className="text-3xl font-bold text-white">My Profile</h1>
      
      <div className="bg-slate-800 p-8 rounded-2xl border border-slate-700 shadow-xl relative overflow-hidden">
        {/* Background decorative element */}
        <div className="absolute top-0 right-0 w-32 h-32 bg-indigo-500/10 rounded-bl-full -mr-8 -mt-8"></div>
        
        <div className="flex items-center gap-6 mb-8 relative z-10">
          <div className="w-20 h-20 bg-gradient-to-br from-indigo-500 to-purple-500 rounded-full flex items-center justify-center text-white text-3xl font-bold shadow-lg">
            {user.username.charAt(0).toUpperCase()}
          </div>
          <div>
            <h2 className="text-2xl font-bold text-white">{user.username}</h2>
            <p className="text-slate-400">OtakuVerse Explorer</p>
          </div>
        </div>

        <div className="space-y-4 relative z-10">
          <div className="flex items-center gap-4 p-4 bg-slate-900/50 rounded-lg">
            <Mail className="text-indigo-400" size={20} />
            <div>
              <div className="text-xs text-slate-500 uppercase font-bold">Email</div>
              <div className="text-slate-200">{user.email}</div>
            </div>
          </div>
          
          <div className="flex items-center gap-4 p-4 bg-slate-900/50 rounded-lg">
            <Shield className="text-purple-400" size={20} />
            <div>
              <div className="text-xs text-slate-500 uppercase font-bold">User ID</div>
              <div className="text-slate-400 font-mono text-xs">{user.id}</div>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-slate-800 p-8 rounded-2xl border border-slate-700">
        <div className="flex items-center gap-2 mb-6">
          <Settings className="text-slate-400" size={20} />
          <h3 className="text-lg font-bold text-white">Account Settings</h3>
        </div>
        
        <div className="space-y-4">
          <div className="flex justify-between items-center p-4 bg-slate-900/30 rounded-lg border border-slate-700/50">
            <div>
              <div className="text-white font-medium">Dark Mode</div>
              <div className="text-sm text-slate-500">Always on for maximum immersion</div>
            </div>
            <div className="w-12 h-6 bg-indigo-600 rounded-full relative">
              <div className="absolute right-1 top-1 w-4 h-4 bg-white rounded-full"></div>
            </div>
          </div>
           <div className="flex justify-between items-center p-4 bg-slate-900/30 rounded-lg border border-slate-700/50">
            <div>
              <div className="text-white font-medium">Notifications</div>
              <div className="text-sm text-slate-500">Email digests about new recommendations</div>
            </div>
            <div className="w-12 h-6 bg-slate-700 rounded-full relative">
              <div className="absolute left-1 top-1 w-4 h-4 bg-slate-400 rounded-full"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;