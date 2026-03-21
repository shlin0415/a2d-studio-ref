/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect } from 'react';
import { 
  Settings, 
  User, 
  Edit3, 
  Play, 
  RefreshCw, 
  ChevronLeft, 
  ChevronRight, 
  MessageSquare, 
  FileText, 
  Share2, 
  Clock, 
  Layout, 
  Users, 
  Library, 
  Layers,
  Download,
  Maximize2,
  Save,
  Eye,
  EyeOff,
  CheckCircle2,
  Plus,
  X,
  Image as ImageIcon,
  Type
} from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';
import { Rnd } from 'react-rnd';

const EMMA_IMG = "https://raw.githubusercontent.com/shlin0415/TmpForIssues/main/Ema.png";
const HIRO_IMG = "https://raw.githubusercontent.com/shlin0415/TmpForIssues/main/Hiro.png";

type RegionType = 'main' | 'dialogue' | 'fig' | 'floating' | 'custom';

interface Region {
  id: string;
  type: RegionType;
  title: string;
  x: number;
  y: number;
  width: number;
  height: number;
  content?: any;
  isVisible: boolean;
}

const DEFAULT_REGIONS: Record<string, Region> = {
  dialogue1: { id: 'dialogue1', type: 'dialogue', title: 'character dialogue region 1', x: 20, y: 20, width: 220, height: 280, isVisible: true, content: { name: 'Emma', text: '"If we process the dimensional shift now..."'} },
  fig1: { id: 'fig1', type: 'fig', title: 'character fig region 1', x: 20, y: 320, width: 220, height: 540, isVisible: true, content: { img: EMMA_IMG, name: 'Emma' } },
  main: { id: 'main', type: 'main', title: 'main text / fig region', x: 260, y: 20, width: 1000, height: 840, isVisible: true },
  floating: { id: 'floating', type: 'floating', title: 'floating region', x: 850, y: 40, width: 380, height: 220, isVisible: true },
  dialogue2: { id: 'dialogue2', type: 'dialogue', title: 'character dialogue region 2', x: 1280, y: 20, width: 220, height: 280, isVisible: true, content: { name: 'Hiro', text: '"I understand the risk, but we have no choice."' } },
  fig2: { id: 'fig2', type: 'fig', title: 'character fig region 2', x: 1280, y: 320, width: 220, height: 540, isVisible: true, content: { img: HIRO_IMG, name: 'Hiro' } },
};

export default function App() {
  const [showSaveFeedback, setShowSaveFeedback] = useState(false);
  const [showAddMenu, setShowAddMenu] = useState(false);

  // Load regions from localStorage or use defaults
  const [regions, setRegions] = useState<Record<string, Region>>(() => {
    const saved = localStorage.getItem('a2d-studio-layout-v2');
    return saved ? JSON.parse(saved) : DEFAULT_REGIONS;
  });

  const updateRegion = (id: string, data: Partial<Region>) => {
    setRegions(prev => ({
      ...prev,
      [id]: { ...prev[id], ...data }
    }));
  };

  const deleteRegion = (id: string) => {
    const newRegions = { ...regions };
    delete newRegions[id];
    setRegions(newRegions);
  };

  const addRegion = (type: RegionType) => {
    const id = `${type}_${Date.now()}`;
    const newRegion: Region = {
      id,
      type,
      title: `${type} region ${Object.keys(regions).length + 1}`,
      x: 100,
      y: 100,
      width: 300,
      height: 200,
      isVisible: true,
      content: type === 'dialogue' ? { name: 'New Character', text: '...' } : type === 'fig' ? { img: '', name: 'Character' } : undefined
    };
    setRegions(prev => ({ ...prev, [id]: newRegion }));
    setShowAddMenu(false);
  };

  const saveLayout = () => {
    localStorage.setItem('a2d-studio-layout-v2', JSON.stringify(regions));
    setShowSaveFeedback(true);
    setTimeout(() => setShowSaveFeedback(false), 2000);
  };

  const resetLayout = () => {
    if (confirm('Reset to default layout?')) {
      setRegions(DEFAULT_REGIONS);
      localStorage.removeItem('a2d-studio-layout-v2');
    }
  };

  return (
    <div className="h-screen w-screen bg-white text-[#1a1a1a] font-sans overflow-hidden flex flex-col">
      {/* Top Bar */}
      <header className="h-12 border-b border-gray-100 px-6 flex items-center justify-between z-50 bg-white/80 backdrop-blur-md">
        <div className="flex items-center gap-8">
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 bg-black rounded flex items-center justify-center">
              <span className="text-white font-black text-[10px]">A2D</span>
            </div>
            <span className="text-sm font-bold tracking-tight text-black uppercase font-mono">a2d-studio</span>
          </div>
          
          <div className="flex items-center gap-4 border-l border-gray-100 pl-4">
            {[Edit3, Play, RefreshCw, ChevronLeft, ChevronRight].map((Icon, i) => (
              <button key={i} className="p-1.5 text-gray-400 hover:text-black transition-colors">
                <Icon size={16} />
              </button>
            ))}
          </div>
        </div>

        <div className="flex items-center gap-3">
          <div className="relative">
            <button 
              onClick={() => setShowAddMenu(!showAddMenu)}
              className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-gray-50 text-gray-600 text-[10px] font-bold hover:bg-gray-100 transition-all border border-gray-200"
            >
              <Plus size={12} />
              Add Region
            </button>
            
            <AnimatePresence>
              {showAddMenu && (
                <motion.div 
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: 10 }}
                  className="absolute top-full mt-2 right-0 w-48 bg-white border border-gray-100 shadow-xl rounded-2xl p-2 z-[100]"
                >
                  <p className="text-[9px] font-bold text-gray-300 uppercase tracking-widest px-3 py-2">Templates</p>
                  {[
                    { type: 'dialogue', icon: MessageSquare, label: 'Dialogue' },
                    { type: 'fig', icon: ImageIcon, label: 'Character Fig' },
                    { type: 'floating', icon: Layers, label: 'Floating' },
                    { type: 'main', icon: Layout, label: 'Main Workspace' },
                    { type: 'custom', icon: Type, label: 'Custom' },
                  ].map((item) => (
                    <button
                      key={item.type}
                      onClick={() => addRegion(item.type as RegionType)}
                      className="w-full flex items-center gap-3 px-3 py-2 hover:bg-gray-50 rounded-xl transition-colors text-left"
                    >
                      <item.icon size={14} className="text-gray-400" />
                      <span className="text-[10px] font-medium text-gray-700">{item.label}</span>
                    </button>
                  ))}
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          <button 
            onClick={resetLayout}
            className="px-3 py-1.5 rounded-full text-[10px] font-bold text-gray-400 hover:text-black transition-colors"
          >
            Reset
          </button>
          
          <button 
            onClick={saveLayout}
            className="flex items-center gap-2 px-4 py-1.5 rounded-full bg-black text-white text-[10px] font-bold hover:bg-gray-800 transition-all shadow-sm active:scale-95"
          >
            {showSaveFeedback ? <CheckCircle2 size={12} /> : <Save size={12} />}
            {showSaveFeedback ? 'Saved!' : 'Apply & Save Preference'}
          </button>
          
          <div className="w-[1px] h-4 bg-gray-100 mx-1" />
          
          <button className="p-1.5 text-gray-400 hover:text-black transition-colors">
            <Settings size={18} />
          </button>
          <button className="p-1.5 text-gray-400 hover:text-black transition-colors">
            <User size={18} />
          </button>
        </div>
      </header>

      <div className="flex-1 relative overflow-auto bg-white p-4">
        {/* The Union Container */}
        <div className="min-w-[1520px] min-h-[880px] relative h-full w-full border border-blue-100/30 rounded-[3rem] bg-gray-50/20">
          
          <AnimatePresence>
            {Object.values(regions).map((region: Region) => (
              <Rnd
                key={region.id}
                size={{ width: region.width, height: region.height }}
                position={{ x: region.x, y: region.y }}
                onDragStop={(e, d) => updateRegion(region.id, { x: d.x, y: d.y })}
                onResizeStop={(e, direction, ref, delta, position) => {
                  updateRegion(region.id, {
                    width: parseInt(ref.style.width),
                    height: parseInt(ref.style.height),
                    ...position,
                  });
                }}
                bounds="parent"
                className="z-20"
              >
                <motion.div 
                  initial={{ opacity: 0, scale: 0.98 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.98 }}
                  className={`w-full h-full bg-white rounded-[2.5rem] border border-gray-200/60 shadow-sm flex flex-col relative group overflow-hidden ${region.type === 'main' ? 'bg-white' : 'bg-white/80 backdrop-blur-sm'}`}
                >
                  {/* Region Header / Label */}
                  <div className="absolute top-6 left-8 right-8 flex justify-between items-center z-10">
                    <div className="text-[9px] font-bold text-gray-300 uppercase tracking-widest cursor-move select-none">
                      {region.title}
                    </div>
                    <div className="flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                      <button 
                        onClick={() => deleteRegion(region.id)}
                        className="p-1 hover:bg-red-50 text-gray-300 hover:text-red-400 rounded-full transition-colors"
                      >
                        <X size={12} />
                      </button>
                    </div>
                  </div>

                  {/* Region Content based on Type */}
                  <div className="flex-1 flex flex-col p-8 pt-14 h-full">
                    {region.type === 'main' && (
                      <div className="flex-1 flex items-center justify-center">
                        <div className="text-center opacity-10 group-hover:opacity-20 transition-opacity">
                          <Layout size={64} className="mx-auto mb-4" />
                          <p className="text-sm uppercase tracking-[0.4em]">Main Workspace</p>
                        </div>
                      </div>
                    )}

                    {region.type === 'dialogue' && (
                      <div className="flex flex-col h-full">
                        <div className="flex items-center gap-2 mb-3">
                          <div className="w-6 h-6 rounded-full bg-gray-50 flex items-center justify-center border border-gray-100">
                            <MessageSquare size={10} className="text-gray-400" />
                          </div>
                          <span className="text-[10px] font-bold text-black uppercase tracking-widest">{region.content?.name}</span>
                        </div>
                        <p className="text-xs font-medium text-gray-700 leading-relaxed italic">
                          {region.content?.text}
                        </p>
                      </div>
                    )}

                    {region.type === 'fig' && (
                      <div className="flex-1 flex flex-col justify-end relative">
                        <div className="absolute inset-0 flex items-center justify-center opacity-5">
                          <ImageIcon size={48} />
                        </div>
                        {region.content?.img ? (
                          <img 
                            src={region.content.img} 
                            alt={region.content.name} 
                            className="h-full w-full object-contain z-10"
                            referrerPolicy="no-referrer"
                          />
                        ) : (
                          <div className="h-full w-full border-2 border-dashed border-gray-100 rounded-3xl flex items-center justify-center text-[10px] text-gray-300 uppercase font-bold">
                            No Image
                          </div>
                        )}
                        <div className="mt-2 text-center">
                          <span className="text-[8px] font-bold text-gray-300 uppercase tracking-tighter">{region.content?.name}</span>
                        </div>
                      </div>
                    )}

                    {region.type === 'floating' && (
                      <div className="flex-1 flex items-center justify-center text-center">
                        <div className="text-gray-400">
                          <p className="text-[10px] leading-relaxed">floating region<br/>which can contain other things<br/>and can be hidden if needed</p>
                        </div>
                      </div>
                    )}

                    {region.type === 'custom' && (
                      <div className="flex-1 border-2 border-dashed border-gray-50 rounded-3xl flex items-center justify-center">
                        <Type size={24} className="text-gray-100" />
                      </div>
                    )}
                  </div>
                </motion.div>
              </Rnd>
            ))}
          </AnimatePresence>

        </div>
      </div>

      {/* Footer */}
      <footer className="h-14 border-t border-gray-100 bg-white flex items-center justify-center gap-12 z-50">
        {[
          { id: 'Timeline', icon: Clock, label: 'Timeline' },
          { id: 'Character', icon: Users, label: 'Character' },
          { id: 'Script', icon: FileText, label: 'Script' },
          { id: 'Export', icon: Share2, label: 'Export' },
        ].map((item) => (
          <button
            key={item.id}
            className="flex items-center gap-2 px-4 py-1.5 rounded-full text-gray-400 hover:text-black hover:bg-gray-50 transition-all"
          >
            <item.icon size={16} />
            <span className="text-[10px] font-bold uppercase tracking-wider">{item.label}</span>
          </button>
        ))}
      </footer>
    </div>
  );
}
