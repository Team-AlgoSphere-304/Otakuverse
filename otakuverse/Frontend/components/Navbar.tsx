import React, { useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/useStore';
import { Menu, X, Rocket, Compass, History as HistoryIcon, User as UserIcon, LogOut, Bookmark, Search } from 'lucide-react';

const Navbar: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const { isAuthenticated, logout, user } = useAuthStore();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const isActive = (path: string) => location.pathname === path;

  const NavLink = ({ to, icon: Icon, label }: { to: string, icon: any, label: string }) => (
    <Link
      to={to}
      className={`flex items-center space-x-2 px-3 py-2 rounded-md transition-colors ${
        isActive(to) 
          ? 'bg-indigo-600 text-white shadow-[0_0_10px_rgba(99,102,241,0.5)]' 
          : 'text-slate-300 hover:bg-slate-800 hover:text-white'
      }`}
      onClick={() => setIsOpen(false)}
    >
      <Icon size={18} />
      <span>{label}</span>
    </Link>
  );

  return (
    <nav className="bg-slate-950 border-b border-slate-800 sticky top-0 z-50">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2 text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 to-purple-500">
            <Rocket className="text-indigo-400" />
            <span>OtakuVerse</span>
          </Link>

          {/* Desktop Nav */}
          <div className="hidden md:flex items-center space-x-4">
            <NavLink to="/search" icon={Search} label="Search" />
            {isAuthenticated ? (
              <>
                <NavLink to="/recommendations" icon={Compass} label="Discover" />
                <NavLink to="/watchlist" icon={Bookmark} label="Watch List" />
                <NavLink to="/history" icon={HistoryIcon} label="History" />
                <div className="h-6 w-px bg-slate-700 mx-2"></div>
                <NavLink to="/profile" icon={UserIcon} label={user?.username || 'Profile'} />
                <button
                  onClick={handleLogout}
                  className="p-2 text-slate-400 hover:text-red-400 transition-colors"
                  title="Logout"
                >
                  <LogOut size={20} />
                </button>
              </>
            ) : (
              <div className="space-x-4">
                <Link to="/login" className="text-slate-300 hover:text-white font-medium">Login</Link>
                <Link to="/register" className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg font-medium transition-colors shadow-lg shadow-indigo-500/20">
                  Get Started
                </Link>
              </div>
            )}
          </div>

          {/* Mobile Menu Button */}
          <div className="md:hidden">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="text-slate-300 hover:text-white focus:outline-none"
            >
              {isOpen ? <X size={24} /> : <Menu size={24} />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Nav */}
      {isOpen && (
        <div className="md:hidden bg-slate-900 border-b border-slate-800">
          <div className="px-4 py-3 space-y-2">
            <NavLink to="/search" icon={Search} label="Search" />
            {isAuthenticated ? (
              <>
                <NavLink to="/recommendations" icon={Compass} label="Discover" />
                <NavLink to="/watchlist" icon={Bookmark} label="Watch List" />
                <NavLink to="/history" icon={HistoryIcon} label="History" />
                <NavLink to="/profile" icon={UserIcon} label="Profile" />
                <button
                  onClick={handleLogout}
                  className="w-full flex items-center space-x-2 px-3 py-2 text-red-400 hover:bg-slate-800 rounded-md"
                >
                  <LogOut size={18} />
                  <span>Logout</span>
                </button>
              </>
            ) : (
              <div className="flex flex-col space-y-3 pt-2">
                <Link 
                  to="/login" 
                  className="block text-center text-slate-300 py-2 border border-slate-700 rounded-lg hover:bg-slate-800"
                  onClick={() => setIsOpen(false)}
                >
                  Login
                </Link>
                <Link 
                  to="/register" 
                  className="block text-center bg-indigo-600 text-white py-2 rounded-lg hover:bg-indigo-700"
                  onClick={() => setIsOpen(false)}
                >
                  Register
                </Link>
              </div>
            )}
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;