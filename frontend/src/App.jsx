import React, { useState, useEffect } from 'react';
import { 
  Wrench, 
  Layers, 
  FileText, 
  LogOut, 
  User, 
  AlertTriangle, 
  CheckCircle, 
  Trash2, 
  Plus, 
  RotateCcw, 
  Boxes,
  Lock,
  Menu,
  X,
  Globe
} from 'lucide-react';

const API_BASE = 'http://localhost:8000';

function App() {
  const [token, setToken] = useState(localStorage.getItem('access_token'));
  const [user, setUser] = useState(null);
  const [activeTab, setActiveTab] = useState('inventory');
  
  // Navigation & UI States
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [mousePos, setMousePos] = useState({ x: -500, y: -500 });

  // Login State
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loginError, setLoginError] = useState('');
  const [loginLoading, setLoginLoading] = useState(false);

  // Data State
  const [inventory, setInventory] = useState(null);
  const [parts, setParts] = useState([]);
  const [assemblies, setAssemblies] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  // Form States
  const [selectedAircraft, setSelectedAircraft] = useState('TB2');
  const [wingPart, setWingPart] = useState('');
  const [fuselagePart, setFuselagePart] = useState('');
  const [tailPart, setTailPart] = useState('');
  const [avionicsPart, setAvionicsPart] = useState('');
  const [partTypeToProduce, setPartTypeToProduce] = useState('');

  const handleMouseMove = (e) => {
    setMousePos({ x: e.clientX, y: e.clientY });
  };

  // Fetch current user profile
  const fetchUserProfile = async (authToken) => {
    try {
      const res = await fetch(`${API_BASE}/api/user/`, {
        headers: { 'Authorization': `Bearer ${authToken}` }
      });
      if (res.ok) {
        const data = await res.json();
        setUser(data);
        const defaultPart = teamToPartType(data.team);
        if (defaultPart) {
          setPartTypeToProduce(defaultPart);
        }
      } else {
        handleLogout();
      }
    } catch (err) {
      console.error(err);
      handleLogout();
    }
  };

  useEffect(() => {
    if (token) {
      fetchUserProfile(token);
    }
  }, [token]);

  // Fetch dashboard data
  useEffect(() => {
    if (token && user) {
      fetchData();
    }
  }, [token, user, activeTab]);

  const fetchData = async () => {
    setLoading(true);
    setError('');
    try {
      const headers = { 'Authorization': `Bearer ${token}` };

      const invRes = await fetch(`${API_BASE}/api/inventory/`, { headers });
      if (invRes.ok) {
        const invData = await invRes.json();
        setInventory(invData);
      }

      if (user.team === 'assemblyTeam' || activeTab === 'aircrafts') {
        const assRes = await fetch(`${API_BASE}/api/assemblies/`, { headers });
        if (assRes.ok) {
          const assData = await assRes.json();
          setAssemblies(assData);
        }
      }

      const partsRes = await fetch(`${API_BASE}/api/parts/`, { headers });
      if (partsRes.ok) {
        const partsData = await partsRes.json();
        setParts(partsData);
      }
    } catch (err) {
      setError('Veriler yüklenirken bir hata oluştu.');
    } finally {
      setLoading(false);
    }
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoginError('');
    setLoginLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/token/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });
      const data = await res.json();
      if (res.ok) {
        localStorage.setItem('access_token', data.access);
        localStorage.setItem('refresh_token', data.refresh);
        setToken(data.access);
        setUsername('');
        setPassword('');
      } else {
        setLoginError(data.detail || 'Giriş bilgileri hatalı.');
      }
    } catch (err) {
      setLoginError('Sunucu bağlantı hatası.');
    } finally {
      setLoginLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setToken(null);
    setUser(null);
    setInventory(null);
    setParts([]);
    setAssemblies([]);
    setActiveTab('inventory');
    setIsMobileMenuOpen(false);
  };

  const teamToPartType = (team) => {
    return {
      'wingTeam': 'wing',
      'fuselageTeam': 'fuselage',
      'tailTeam': 'tail',
      'avionicsTeam': 'avionics',
    }[team];
  };

  const getTeamLabel = (team) => {
    return {
      'wingTeam': 'Kanat Takımı',
      'fuselageTeam': 'Gövde Takımı',
      'tailTeam': 'Kuyruk Takımı',
      'avionicsTeam': 'Aviyonik Takımı',
      'assemblyTeam': 'Montaj Takımı',
    }[team] || team;
  };

  const getPartLabel = (name) => {
    return {
      'wing': 'Kanat',
      'fuselage': 'Gövde',
      'tail': 'Kuyruk',
      'avionics': 'Aviyonik',
    }[name] || name;
  };

  const handleProducePart = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    try {
      const res = await fetch(`${API_BASE}/api/parts/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          name: partTypeToProduce,
          aircraft_type: selectedAircraft
        })
      });
      const data = await res.json();
      if (res.ok) {
        setSuccess(`${selectedAircraft} için ${getPartLabel(partTypeToProduce)} parçası başarıyla üretildi.`);
        fetchData();
      } else {
        setError(data.detail || Object.values(data).flat().join(' '));
      }
    } catch (err) {
      setError('İşlem sırasında bir hata oluştu.');
    }
  };

  const handleRecyclePart = async (partId) => {
    if (!window.confirm('Bu parçayı geri dönüşüme göndermek istediğinize emin misiniz?')) {
      return;
    }
    setError('');
    setSuccess('');
    try {
      const res = await fetch(`${API_BASE}/api/parts/${partId}/`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.ok) {
        setSuccess('Parça başarıyla geri dönüşüme gönderildi.');
        fetchData();
      } else {
        const data = await res.json();
        setError(data.detail || 'Parça geri dönüşüme gönderilemedi.');
      }
    } catch (err) {
      setError('İşlem sırasında bir hata oluştu.');
    }
  };

  const handleAssembleAircraft = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    if (!wingPart || !fuselagePart || !tailPart || !avionicsPart) {
      setError('Lütfen tüm gerekli parçaları seçin.');
      return;
    }

    try {
      const res = await fetch(`${API_BASE}/api/assemblies/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          aircraft_type: selectedAircraft,
          wing: wingPart,
          fuselage: fuselagePart,
          tail: tailPart,
          avionics: avionicsPart
        })
      });
      const data = await res.json();
      if (res.ok) {
        setSuccess(`${selectedAircraft} uçağının montajı başarıyla tamamlandı!`);
        setWingPart('');
        setFuselagePart('');
        setTailPart('');
        setAvionicsPart('');
        fetchData();
      } else {
        setError(data.detail || Object.values(data).flat().join(' '));
      }
    } catch (err) {
      setError('Montaj sırasında bir hata oluştu.');
    }
  };

  const getAvailableParts = (partName, aircraftType) => {
    return parts.filter(p => 
      p.name === partName && 
      p.aircraft_type === aircraftType && 
      !p.is_used && 
      !p.is_recycled
    );
  };

  // Login View
  if (!token || !user) {
    return (
      <div 
        onMouseMove={handleMouseMove}
        className="min-h-screen flex items-center justify-center bg-navy-950 relative overflow-hidden px-4 grid-bg"
      >
        {/* Interactive mouse follower glow (Subtle solid glow) */}
        <div 
          className="pointer-events-none fixed w-[280px] h-[280px] rounded-full bg-cyan-500/5 blur-[80px] transition-transform duration-75 z-0"
          style={{
            left: `${mousePos.x - 140}px`,
            top: `${mousePos.y - 140}px`
          }}
        />

        <div className="w-full max-w-md glass-card rounded-2xl p-8 space-y-6 relative z-10">
          <div className="text-center space-y-2">
            <div className="inline-flex p-3 bg-navy-900 border border-white/10 rounded-2xl text-cyan-400 mb-2">
              <Boxes className="h-8 w-8" />
            </div>
            <h2 className="text-2xl font-bold text-white tracking-wider uppercase">BAYKAR Üretim Portalı</h2>
            <p className="text-[10px] text-cyan-400 font-extrabold tracking-widest">MİLLİ TEKNOLOJİ HAMLESİ</p>
          </div>

          {loginError && (
            <div className="bg-red-500/10 border border-red-500/20 text-red-400 p-3.5 rounded-xl text-xs flex items-center gap-2.5">
              <AlertTriangle className="h-4 w-4 shrink-0" />
              <span>{loginError}</span>
            </div>
          )}

          <form onSubmit={handleLogin} className="space-y-4">
            <div className="space-y-1.5">
              <label className="text-[10px] font-bold uppercase tracking-wider text-gray-400">Kullanıcı Adı</label>
              <input 
                type="text" 
                required
                placeholder="örn: wing_worker"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full glass-input rounded-xl px-4 py-3 text-white placeholder-gray-600 focus:outline-none transition-all text-sm"
              />
            </div>

            <div className="space-y-1.5">
              <label className="text-[10px] font-bold uppercase tracking-wider text-gray-400">Şifre</label>
              <input 
                type="password" 
                required
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full glass-input rounded-xl px-4 py-3 text-white placeholder-gray-600 focus:outline-none transition-all text-sm"
              />
            </div>

            <button 
              type="submit" 
              disabled={loginLoading}
              className="w-full bg-cyan-500 hover:bg-cyan-600 text-navy-950 font-bold py-3.5 rounded-xl transition-all shadow-md active:scale-[0.98] disabled:opacity-50 text-sm flex items-center justify-center gap-2"
            >
              <Lock className="h-4 w-4" />
              {loginLoading ? 'Giriş Yapılıyor...' : 'Giriş Yap'}
            </button>
          </form>
        </div>
      </div>
    );
  }

  // Dashboard View
  return (
    <div 
      onMouseMove={handleMouseMove}
      className="min-h-screen bg-navy-950 text-gray-200 flex flex-col relative overflow-hidden grid-bg"
    >
      {/* Interactive mouse follower glow */}
      <div 
        className="pointer-events-none fixed w-[300px] h-[300px] rounded-full bg-cyan-500/5 blur-[90px] transition-transform duration-75 z-0"
        style={{
          left: `${mousePos.x - 150}px`,
          top: `${mousePos.y - 150}px`
        }}
      />

      {/* Header (Top Horizontal Navbar with Mobile Sandwich) */}
      <header className="bg-navy-900 border-b border-white/10 sticky top-0 z-50 px-6 py-4 shadow-xl">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          {/* Logo */}
          <div className="flex items-center gap-3">
            <div className="p-2 bg-navy-800 border border-white/10 rounded-xl text-cyan-400">
              <Boxes className="h-5 w-5" />
            </div>
            <div>
              <h1 className="text-sm font-bold text-white tracking-widest uppercase">BAYKAR HAVA ARACI ÜRETİMİ</h1>
              <p className="text-[8px] text-cyan-400 font-extrabold tracking-widest">PORTALI</p>
            </div>
          </div>

          {/* Desktop Navigation Links */}
          <nav className="hidden md:flex items-center gap-6">
            <button 
              onClick={() => setActiveTab('inventory')}
              className={`pb-1 text-xs font-bold uppercase tracking-wider border-b-2 transition-all ${activeTab === 'inventory' ? 'border-cyan-500 text-cyan-400' : 'border-transparent text-gray-400 hover:text-white'}`}
            >
              Envanter Durumu
            </button>

            {user.team !== 'assemblyTeam' && (
              <button 
                onClick={() => setActiveTab('production')}
                className={`pb-1 text-xs font-bold uppercase tracking-wider border-b-2 transition-all ${activeTab === 'production' ? 'border-cyan-500 text-cyan-400' : 'border-transparent text-gray-400 hover:text-white'}`}
              >
                Parça Üretimi
              </button>
            )}

            {user.team === 'assemblyTeam' && (
              <button 
                onClick={() => setActiveTab('assembly')}
                className={`pb-1 text-xs font-bold uppercase tracking-wider border-b-2 transition-all ${activeTab === 'assembly' ? 'border-cyan-500 text-cyan-400' : 'border-transparent text-gray-400 hover:text-white'}`}
              >
                Uçak Montajı
              </button>
            )}

            <button 
              onClick={() => setActiveTab('aircrafts')}
              className={`pb-1 text-xs font-bold uppercase tracking-wider border-b-2 transition-all ${activeTab === 'aircrafts' ? 'border-cyan-500 text-cyan-400' : 'border-transparent text-gray-400 hover:text-white'}`}
            >
              Üretilen Uçaklar
            </button>
          </nav>

          {/* User Profile + Logout */}
          <div className="hidden md:flex items-center gap-4">
            <div className="text-right">
              <div className="text-xs font-bold text-white">{user.username}</div>
              <div className="text-[9px] text-cyan-400 font-extrabold uppercase tracking-widest">{getTeamLabel(user.team)}</div>
            </div>
            <button 
              onClick={handleLogout}
              className="p-2 bg-navy-800 hover:bg-red-500/10 hover:text-red-400 border border-white/10 hover:border-red-500/20 rounded-xl transition-all"
              title="Çıkış Yap"
            >
              <LogOut className="h-4 w-4" />
            </button>
          </div>

          {/* Mobile Menu Button (Hamburger Menu) */}
          <div className="flex md:hidden items-center gap-3">
            <button 
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              className="p-2 bg-navy-800 border border-white/10 rounded-xl text-gray-300"
            >
              {isMobileMenuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
            </button>
          </div>
        </div>

        {/* Mobile Dropdown (Sandwich Menu) */}
        {isMobileMenuOpen && (
          <nav className="md:hidden mt-4 pt-4 border-t border-white/5 flex flex-col gap-3">
            <button 
              onClick={() => { setActiveTab('inventory'); setIsMobileMenuOpen(false); }}
              className={`px-4 py-2.5 rounded-xl text-xs font-bold uppercase tracking-wider text-left transition-all ${activeTab === 'inventory' ? 'bg-cyan-500 text-navy-950 font-black' : 'text-gray-400 hover:bg-white/5'}`}
            >
              Envanter Durumu
            </button>

            {user.team !== 'assemblyTeam' && (
              <button 
                onClick={() => { setActiveTab('production'); setIsMobileMenuOpen(false); }}
                className={`px-4 py-2.5 rounded-xl text-xs font-bold uppercase tracking-wider text-left transition-all ${activeTab === 'production' ? 'bg-cyan-500 text-navy-950 font-black' : 'text-gray-400 hover:bg-white/5'}`}
              >
                Parça Üretimi
              </button>
            )}

            {user.team === 'assemblyTeam' && (
              <button 
                onClick={() => { setActiveTab('assembly'); setIsMobileMenuOpen(false); }}
                className={`px-4 py-2.5 rounded-xl text-xs font-bold uppercase tracking-wider text-left transition-all ${activeTab === 'assembly' ? 'bg-cyan-500 text-navy-950 font-black' : 'text-gray-400 hover:bg-white/5'}`}
              >
                Uçak Montajı
              </button>
            )}

            <button 
              onClick={() => { setActiveTab('aircrafts'); setIsMobileMenuOpen(false); }}
              className={`px-4 py-2.5 rounded-xl text-xs font-bold uppercase tracking-wider text-left transition-all ${activeTab === 'aircrafts' ? 'bg-cyan-500 text-navy-950 font-black' : 'text-gray-400 hover:bg-white/5'}`}
            >
              Üretilen Uçaklar
            </button>

            <div className="border-t border-white/5 pt-3 flex items-center justify-between px-4">
              <div>
                <div className="text-xs font-bold text-white">{user.username}</div>
                <div className="text-[9px] text-cyan-400 font-extrabold uppercase tracking-widest">{getTeamLabel(user.team)}</div>
              </div>
              <button 
                onClick={handleLogout}
                className="p-2 bg-navy-800 hover:bg-red-500/10 hover:text-red-400 border border-white/10 rounded-xl transition-all"
              >
                <LogOut className="h-4 w-4" />
              </button>
            </div>
          </nav>
        )}
      </header>

      {/* Content Area */}
      <main className="flex-1 p-6 space-y-6 overflow-y-auto max-w-7xl mx-auto w-full relative z-10">

        {/* Feedback alerts */}
        {error && (
          <div className="bg-red-500/10 border border-red-500/20 text-red-400 p-4 rounded-2xl text-xs font-semibold flex items-start gap-3 backdrop-blur-md">
            <AlertTriangle className="h-4 w-4 shrink-0 mt-0.5" />
            <div>
              <div className="font-bold uppercase tracking-wider">İşlem Başarısız</div>
              <div className="mt-0.5 opacity-90">{error}</div>
            </div>
          </div>
        )}

        {success && (
          <div className="bg-green-500/10 border border-green-500/20 text-green-400 p-4 rounded-2xl text-xs font-semibold flex items-start gap-3 backdrop-blur-md">
            <CheckCircle className="h-4 w-4 shrink-0 mt-0.5" />
            <div>
              <div className="font-bold uppercase tracking-wider">İşlem Başarılı</div>
              <div className="mt-0.5 opacity-90">{success}</div>
            </div>
          </div>
        )}

        {/* TAB: INVENTORY */}
        {activeTab === 'inventory' && (
          <div className="space-y-6">
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
              <div>
                <h2 className="text-xl font-bold text-white uppercase tracking-wider">Hava Aracı Stok Durumu</h2>
                <p className="text-xs text-navy-300">Aktif kullanılabilir montaj parçaları tablosu</p>
              </div>
              <button 
                onClick={fetchData} 
                className="px-4 py-2 bg-navy-800/40 hover:bg-white/5 border border-white/10 rounded-xl text-xs font-extrabold uppercase tracking-widest flex items-center justify-center gap-2 transition-all self-start sm:self-auto"
              >
                <RotateCcw className="h-3.5 w-3.5" /> Yenile
              </button>
            </div>

            {inventory && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {Object.entries(inventory).map(([key, value]) => {
                  const hasWarning = !value.can_assemble;
                  return (
                    <div key={key} className={`glass-card rounded-2xl p-6 space-y-5 transition-all duration-350 hover:translate-y-[-1px] ${hasWarning ? 'border-amber-500/20' : ''}`}>
                      <div className="flex items-center justify-between">
                        <div>
                          <h3 className="text-base font-bold text-white">{value.name}</h3>
                          <span className={`inline-block mt-1 text-[9px] px-2.5 py-0.5 rounded-full font-extrabold uppercase tracking-widest ${value.can_assemble ? 'bg-cyan-500/10 text-cyan-400 border border-cyan-500/20' : 'bg-amber-500/10 text-amber-400 border border-amber-500/20'}`}>
                            {value.can_assemble ? 'Montaja Uygun' : 'Montaj İçin Eksik Var'}
                          </span>
                        </div>
                        {hasWarning && (
                          <div className="flex items-center gap-1 text-amber-400 bg-amber-500/10 border border-amber-500/20 px-2.5 py-1 rounded-xl text-[9px] font-extrabold uppercase tracking-wider">
                            <AlertTriangle className="h-3.5 w-3.5" />
                            <span>Eksik</span>
                          </div>
                        )}
                      </div>

                      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                        {Object.entries(value.stock).map(([pKey, pVal]) => (
                          <div key={pKey} className="bg-space-950/40 border border-white/5 p-3 rounded-2xl text-center space-y-1.5 backdrop-blur-md shadow-inner">
                            <div className="text-[9px] text-gray-400 font-extrabold uppercase tracking-widest">{getPartLabel(pKey)}</div>
                            <div className={`text-2xl font-black ${pVal === 0 ? 'text-red-400' : 'text-white'}`}>{pVal}</div>
                          </div>
                        ))}
                      </div>

                      {hasWarning && (
                        <div className="text-xs bg-amber-500/5 border border-amber-500/15 text-amber-300/80 p-3.5 rounded-2xl">
                          <strong>Uçak Montajı Yapılamıyor:</strong> Stokta <span className="font-bold text-amber-400">{value.missing_parts.join(', ')}</span> parçaları eksik.
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        )}

        {/* TAB: PRODUCTION */}
        {activeTab === 'production' && user.team !== 'assemblyTeam' && (
          <div className="space-y-6 animate-fadeIn">
            <div className="glass-card rounded-2xl p-6 shadow-xl">
              <h3 className="text-base font-bold text-white mb-4 uppercase tracking-widest text-cyan-400">Parça Üretim İstasyonu</h3>
              <form onSubmit={handleProducePart} className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 items-end gap-4">
                <div className="space-y-1.5">
                  <label className="text-[9px] font-extrabold uppercase tracking-widest text-gray-400">Uçak Tipi</label>
                  <select 
                    value={selectedAircraft}
                    onChange={(e) => setSelectedAircraft(e.target.value)}
                    className="w-full glass-input rounded-xl px-4 py-2.5 text-white focus:outline-none transition-all text-sm font-semibold"
                  >
                    <option value="TB2">TB2</option>
                    <option value="TB3">TB3</option>
                    <option value="AKINCI">AKINCI</option>
                    <option value="KIZILELMA">KIZILELMA</option>
                  </select>
                </div>

                <div className="space-y-1.5">
                  <label className="text-[9px] font-extrabold uppercase tracking-widest text-gray-400">Üretilecek Parça</label>
                  <div className="w-full bg-space-950/40 border border-white/10 text-cyan-400 rounded-xl px-4 py-2.5 text-sm font-black uppercase tracking-widest shadow-inner">
                    {getPartLabel(teamToPartType(user.team))}
                  </div>
                </div>

                <button 
                  type="submit" 
                  className="bg-cyan-500 hover:bg-cyan-600 text-navy-950 font-bold py-2.5 px-4 rounded-xl transition-all shadow-md flex items-center justify-center gap-2 text-sm uppercase tracking-wider active:scale-95"
                >
                  <Plus className="h-4 w-4" /> Parça Üretimini Başlat
                </button>
              </form>
            </div>

            {/* Created Parts Log */}
            <div className="glass-card rounded-2xl p-6 shadow-xl space-y-4">
              <h3 className="text-base font-bold text-white uppercase tracking-widest">Üretim Geçmişi</h3>
              <div className="overflow-x-auto">
                <table className="w-full text-left border-collapse">
                  <thead>
                    <tr className="border-b border-white/10 text-gray-400 text-[10px] font-bold uppercase tracking-widest">
                      <th className="pb-3">Parça ID</th>
                      <th className="pb-3">Parça Tipi</th>
                      <th className="pb-3">Uçak Modeli</th>
                      <th className="pb-3">Durum</th>
                      <th className="pb-3 text-right">Eylemler</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-white/5 text-sm">
                    {parts
                      .filter(p => p.created_by === user.id)
                      .map(part => (
                        <tr key={part.id} className="hover:bg-white/5 transition-colors">
                          <td className="py-3 font-bold text-cyan-400">#{part.id}</td>
                          <td className="py-3 font-bold">{part.name_display}</td>
                          <td className="py-3">{part.aircraft_type_display}</td>
                          <td className="py-3">
                            {part.is_used ? (
                              <span className="text-[9px] bg-green-500/10 text-green-400 border border-green-500/15 px-2 py-0.5 rounded font-bold uppercase tracking-widest">Kullanıldı</span>
                            ) : part.is_recycled ? (
                              <span className="text-[9px] bg-red-500/10 text-red-400 border border-red-500/15 px-2 py-0.5 rounded font-bold uppercase tracking-widest">Geri Dönüşüm</span>
                            ) : (
                              <span className="text-[9px] bg-blue-500/10 text-blue-400 border border-blue-500/15 px-2 py-0.5 rounded font-bold uppercase tracking-widest">Stokta</span>
                            )}
                          </td>
                          <td className="py-3 text-right">
                            {!part.is_used && !part.is_recycled && (
                              <button 
                                onClick={() => handleRecyclePart(part.id)}
                                className="p-1.5 bg-red-500/10 hover:bg-red-500/20 text-red-400 rounded-lg hover:border border-red-500/20 transition-all active:scale-95"
                                title="Geri Dönüşüme Gönder (Sil)"
                              >
                                <Trash2 className="h-3.5 w-3.5" />
                              </button>
                            )}
                          </td>
                        </tr>
                      ))}
                    {parts.filter(p => p.created_by === user.id).length === 0 && (
                      <tr>
                        <td colSpan="5" className="text-center py-6 text-navy-400">Üretim kaydınız bulunmamaktadır.</td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* TAB: ASSEMBLY */}
        {activeTab === 'assembly' && user.team === 'assemblyTeam' && (
          <div className="space-y-6 animate-fadeIn">
            <div className="glass-card rounded-2xl p-6 shadow-xl space-y-6">
              <h3 className="text-base font-bold text-white uppercase tracking-widest">Uçak Montaj İstasyonu</h3>
              
              <form onSubmit={handleAssembleAircraft} className="space-y-6">
                <div className="max-w-xs space-y-1.5">
                  <label className="text-[9px] font-bold uppercase tracking-widest text-gray-400">Montajlanacak Uçak Tipi</label>
                  <select 
                    value={selectedAircraft}
                    onChange={(e) => {
                      setSelectedAircraft(e.target.value);
                      setWingPart('');
                      setFuselagePart('');
                      setTailPart('');
                      setAvionicsPart('');
                    }}
                    className="w-full glass-input rounded-xl px-4 py-2.5 text-white focus:outline-none transition-all text-sm font-semibold"
                  >
                    <option value="TB2">TB2</option>
                    <option value="TB3">TB3</option>
                    <option value="AKINCI">AKINCI</option>
                    <option value="KIZILELMA">KIZILELMA</option>
                  </select>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                  {/* Wing */}
                  <div className="space-y-2 bg-space-950/40 p-4 border border-white/15 rounded-2xl shadow-inner">
                    <label className="text-[10px] font-bold uppercase tracking-widest text-gray-400">Kanat Seçimi</label>
                    <select 
                      value={wingPart}
                      onChange={(e) => setWingPart(e.target.value)}
                      className="w-full bg-space-900/40 border border-white/10 rounded-lg p-2 text-white text-xs font-semibold focus:outline-none focus:border-cyan-400"
                    >
                      <option value="">-- Seçiniz --</option>
                      {getAvailableParts('wing', selectedAircraft).map(p => (
                        <option key={p.id} value={p.id}>#{p.id} - ({p.created_by_username})</option>
                      ))}
                    </select>
                    <div className="text-[10px] text-navy-400">Uygun Adet: {getAvailableParts('wing', selectedAircraft).length}</div>
                  </div>

                  {/* Fuselage */}
                  <div className="space-y-2 bg-space-950/40 p-4 border border-white/15 rounded-2xl shadow-inner">
                    <label className="text-[10px] font-bold uppercase tracking-widest text-gray-400">Gövde Seçimi</label>
                    <select 
                      value={fuselagePart}
                      onChange={(e) => setFuselagePart(e.target.value)}
                      className="w-full bg-space-900/40 border border-white/10 rounded-lg p-2 text-white text-xs font-semibold focus:outline-none focus:border-cyan-400"
                    >
                      <option value="">-- Seçiniz --</option>
                      {getAvailableParts('fuselage', selectedAircraft).map(p => (
                        <option key={p.id} value={p.id}>#{p.id} - ({p.created_by_username})</option>
                      ))}
                    </select>
                    <div className="text-[10px] text-navy-400">Uygun Adet: {getAvailableParts('fuselage', selectedAircraft).length}</div>
                  </div>

                  {/* Tail */}
                  <div className="space-y-2 bg-space-950/40 p-4 border border-white/15 rounded-2xl shadow-inner">
                    <label className="text-[10px] font-bold uppercase tracking-widest text-gray-400">Kuyruk Seçimi</label>
                    <select 
                      value={tailPart}
                      onChange={(e) => setTailPart(e.target.value)}
                      className="w-full bg-space-900/40 border border-white/10 rounded-lg p-2 text-white text-xs font-semibold focus:outline-none focus:border-cyan-400"
                    >
                      <option value="">-- Seçiniz --</option>
                      {getAvailableParts('tail', selectedAircraft).map(p => (
                        <option key={p.id} value={p.id}>#{p.id} - ({p.created_by_username})</option>
                      ))}
                    </select>
                    <div className="text-[10px] text-navy-400">Uygun Adet: {getAvailableParts('tail', selectedAircraft).length}</div>
                  </div>

                  {/* Avionics */}
                  <div className="space-y-2 bg-space-950/40 p-4 border border-white/15 rounded-2xl shadow-inner">
                    <label className="text-[10px] font-bold uppercase tracking-widest text-gray-400">Aviyonik Seçimi</label>
                    <select 
                      value={avionicsPart}
                      onChange={(e) => setAvionicsPart(e.target.value)}
                      className="w-full bg-space-900/40 border border-white/10 rounded-lg p-2 text-white text-xs font-semibold focus:outline-none focus:border-cyan-400"
                    >
                      <option value="">-- Seçiniz --</option>
                      {getAvailableParts('avionics', selectedAircraft).map(p => (
                        <option key={p.id} value={p.id}>#{p.id} - ({p.created_by_username})</option>
                      ))}
                    </select>
                    <div className="text-[10px] text-navy-400">Uygun Adet: {getAvailableParts('avionics', selectedAircraft).length}</div>
                  </div>
                </div>

                <button 
                  type="submit" 
                  className="bg-cyan-500 hover:bg-cyan-600 text-navy-950 font-bold py-3 px-6 rounded-xl transition-all shadow-md flex items-center justify-center gap-2 text-sm uppercase tracking-wider active:scale-95"
                >
                  <Layers className="h-4 w-4" /> Hava Aracını Montajla ve Üretimi Tamamla
                </button>
              </form>
            </div>
          </div>
        )}

        {/* TAB: AIRCRAFTS LIST */}
        {activeTab === 'aircrafts' && (
          <div className="space-y-6 animate-fadeIn">
            <div className="glass-card rounded-2xl p-6 shadow-xl">
              <h3 className="text-base font-bold text-white mb-4 uppercase tracking-widest font-bold">Üretilen Hava Araçları</h3>
              <div className="overflow-x-auto">
                <table className="w-full text-left border-collapse">
                  <thead>
                    <tr className="border-b border-white/10 text-gray-400 text-[10px] font-bold uppercase tracking-widest">
                      <th className="pb-3">Montaj No</th>
                      <th className="pb-3">Uçak Modeli</th>
                      <th className="pb-3">Kullanılan Parçalar (ID)</th>
                      <th className="pb-3">Montajlayan Personel</th>
                      <th className="pb-3">Montaj Tarihi</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-white/5 text-sm">
                    {assemblies.map(ass => (
                      <tr key={ass.id} className="hover:bg-white/5 transition-colors">
                        <td className="py-4 font-bold text-gray-400">#{ass.id}</td>
                        <td className="py-4 font-bold text-cyan-400">{ass.aircraft_type_display}</td>
                        <td className="py-4">
                          <div className="grid grid-cols-2 gap-x-4 gap-y-1 text-xs">
                            <div><span className="text-gray-400">Kanat:</span> #{ass.wing}</div>
                            <div><span className="text-gray-400">Gövde:</span> #{ass.fuselage}</div>
                            <div><span className="text-gray-400">Kuyruk:</span> #{ass.tail}</div>
                            <div><span className="text-gray-400">Aviyonik:</span> #{ass.avionics}</div>
                          </div>
                        </td>
                        <td className="py-4 font-bold">{ass.employee_username}</td>
                        <td className="py-4 text-xs text-navy-300">
                          {new Date(ass.assembled_at).toLocaleString('tr-TR')}
                        </td>
                      </tr>
                    ))}
                    {assemblies.length === 0 && (
                      <tr>
                        <td colSpan="5" className="text-center py-6 text-navy-400">Üretim tamamlanan hava aracı bulunmamaktadır.</td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

      </main>

      {/* Footer (New Component) */}
      <footer className="bg-navy-900 border-t border-white/10 mt-auto py-8 px-6 text-gray-400 text-xs">
        <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* About Column */}
          <div className="space-y-2">
            <h4 className="font-bold text-white uppercase tracking-wider text-xs flex items-center gap-2">
              <Boxes className="h-4 w-4 text-cyan-400" />
              BAYKAR Hava Aracı Üretim Portalı
            </h4>
            <p className="leading-relaxed opacity-80 text-justify">
              Bu portal; insansız hava araçlarının (TB2, TB3, AKINCI, KIZILELMA) montaj ve üretim parçalarının 
              stok ve üretim kısıtlamalarını denetlemek, personel takımlarının sorumluluk sınırları dahilinde parça 
              üretimini yönetmek amacıyla kurumsal standartlarda geliştirilmiştir.
            </p>
          </div>

          {/* Developer / About Me Column */}
          <div className="space-y-2">
            <h4 className="font-bold text-white uppercase tracking-wider text-xs">
              Geliştirici Hakkında
            </h4>
            <p className="leading-relaxed opacity-80 text-justify">
              <strong>Hüseyin Taşkın</strong> — Arka Uç Yazılım Uzmanı. 
              Marmara Üniversitesi Bilgisayar Mühendisliği mezunudur. Python, Django, REST API ve mikroservis mimarileri 
              konusunda deneyimlidir.
            </p>
            <div className="flex items-center gap-3 pt-1">
              <a 
                href="https://github.com/huseyintaskinn" 
                target="_blank" 
                rel="noreferrer" 
                className="hover:text-white transition-colors"
                title="GitHub"
              >
                <svg className="h-4 w-4 fill-current" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
              </a>
              <a 
                href="https://linkedin.com/in/huseyintaskin023" 
                target="_blank" 
                rel="noreferrer" 
                className="hover:text-white transition-colors"
                title="LinkedIn"
              >
                <svg className="h-4 w-4 fill-current" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.779-1.75-1.75s.784-1.75 1.75-1.75 1.75.779 1.75 1.75-.784 1.75-1.75 1.75zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/></svg>
              </a>
              <a 
                href="https://huseyintaskin.com.tr" 
                target="_blank" 
                rel="noreferrer" 
                className="hover:text-white transition-colors"
                title="Web Sitesi"
              >
                <Globe className="h-4 w-4" />
              </a>
            </div>
          </div>

          {/* Quick Links Column */}
          <div className="space-y-2">
            <h4 className="font-bold text-white uppercase tracking-wider text-xs">
              Hızlı Erişim & Bağlantılar
            </h4>
            <ul className="grid grid-cols-2 gap-x-4 gap-y-1.5">
              <li>
                <button 
                  onClick={() => setActiveTab('inventory')}
                  className="hover:text-white transition-colors text-left"
                >
                  Envanter Durumu
                </button>
              </li>
              {user.team !== 'assemblyTeam' ? (
                <li>
                  <button 
                    onClick={() => setActiveTab('production')}
                    className="hover:text-white transition-colors text-left"
                  >
                    Parça Üretimi
                  </button>
                </li>
              ) : (
                <li>
                  <button 
                    onClick={() => setActiveTab('assembly')}
                    className="hover:text-white transition-colors text-left"
                  >
                    Uçak Montajı
                  </button>
                </li>
              )}
              <li>
                <button 
                  onClick={() => setActiveTab('aircrafts')}
                  className="hover:text-white transition-colors text-left"
                >
                  Üretilen Uçaklar
                </button>
              </li>
              <li>
                <a 
                  href={`${API_BASE}/swagger/`} 
                  target="_blank" 
                  rel="noreferrer" 
                  className="hover:text-white transition-colors"
                >
                  Swagger API Docs
                </a>
              </li>
            </ul>
          </div>
        </div>

        <div className="max-w-7xl mx-auto border-t border-white/5 mt-8 pt-4 text-center text-[10px] text-gray-500">
          &copy; {new Date().getFullYear()} BAYKAR Hava Aracı Üretim Portalı. Hüseyin Taşkın tarafından geliştirilmiştir. Tüm Hakları Saklıdır.
        </div>
      </footer>
    </div>
  );
}

export default App;
