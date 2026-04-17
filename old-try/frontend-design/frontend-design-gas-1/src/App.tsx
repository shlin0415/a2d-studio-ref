/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useRef } from 'react';
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
  Maximize2
} from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';
import { Rnd } from 'react-rnd';

const EMMA_IMG = "https://raw.githubusercontent.com/shlin0415/TmpForIssues/main/Ema.png";
const HIRO_IMG = "https://raw.githubusercontent.com/shlin0415/TmpForIssues/main/Hiro.png";

export default function App() {
  const [activeTab, setActiveTab] = useState('Studio');
  const [activeControl, setActiveControl] = useState('Edit');

  // Initial states for regions
  const [regions, setRegions] = useState({
    mainContent: { x: 20, y: 20, width: 800, height: 400 },
    chatLayer: { x: 20, y: 440, width: 800, height: 200 },
    functionRegion: { x: 840, y: 20, width: 360, height: 140 },
    timelineRegion: { x: 840, y: 180, width: 360, height: 100 },
    characterFigRegion: { x: 840, y: 300, width: 360, height: 340 },
  });

  const updateRegion = (id: string, data: any) => {
    setRegions(prev => ({
      ...prev,
      [id]: { ...prev[id as keyof typeof prev], ...data }
    }));
  };

  return (
    <div className="h-screen w-screen bg-[#0c0e10] text-[#eeeef0] font-sans overflow-hidden flex flex-col">
      {/* Top Navigation Bar */}
      <header className="h-14 border-b border-white/5 px-6 flex items-center justify-between z-50 bg-[#0c0e10]/80 backdrop-blur-md">
        <div className="flex items-center gap-10">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-[#00D4FF] rounded flex items-center justify-center">
              <span className="text-black font-black text-xs">A2D</span>
            </div>
            <span className="text-xl font-bold tracking-tighter text-[#00D4FF] uppercase font-mono">a2d-studio</span>
          </div>
          
          <nav className="flex items-center gap-6">
            {['Studio', 'Characters', 'Library', 'Timeline'].map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`text-sm font-medium transition-all relative py-1 ${
                  activeTab === tab ? 'text-[#00D4FF]' : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                {tab}
                {activeTab === tab && (
                  <motion.div 
                    layoutId="activeTab"
                    className="absolute -bottom-1 left-0 right-0 h-0.5 bg-[#00D4FF]"
                  />
                )}
              </button>
            ))}
          </nav>
        </div>

        <div className="flex items-center gap-4">
          <button className="flex items-center gap-2 px-4 py-1.5 rounded-lg bg-[#232629] text-[#00D4FF] text-xs font-bold hover:bg-[#2d3135] transition-colors border border-white/5">
            <Download size={14} />
            Export to Figma
          </button>
          <button className="p-1.5 text-slate-400 hover:text-white transition-colors">
            <Settings size={20} />
          </button>
          <button className="p-1.5 text-slate-400 hover:text-white transition-colors">
            <User size={20} />
          </button>
        </div>
      </header>

      <div className="flex-1 flex relative overflow-hidden">
        {/* Left Sidebar - Control Region */}
        <aside className="w-20 border-r border-white/5 flex flex-col items-center py-6 gap-6 z-40 bg-[#0c0e10]/40 backdrop-blur-sm">
          <div className="mb-4 text-center">
            <p className="text-[#00D4FF] font-black text-[10px] tracking-tighter">A2D</p>
            <p className="text-[8px] text-slate-500 tracking-widest uppercase">Control</p>
          </div>

          <div className="flex flex-col gap-4 w-full px-3">
            {[
              { id: 'Edit', icon: Edit3, label: 'Edit' },
              { id: 'Run', icon: Play, label: 'Run' },
              { id: 'Auto', icon: RefreshCw, label: 'Auto' },
              { id: 'Step', icon: ChevronLeft, label: 'Step' },
              { id: 'Next', icon: ChevronRight, label: 'Next' },
            ].map((control) => (
              <button
                key={control.id}
                onClick={() => setActiveControl(control.id)}
                className={`flex flex-col items-center gap-1 py-3 rounded-xl transition-all group ${
                  activeControl === control.id 
                    ? 'bg-[#00D4FF]/10 text-[#00D4FF] border border-[#00D4FF]/20' 
                    : 'text-slate-500 hover:text-[#00D4FF] hover:bg-white/5'
                }`}
              >
                <control.icon size={22} strokeWidth={activeControl === control.id ? 2.5 : 2} />
                <span className="text-[8px] font-bold uppercase tracking-widest">{control.label}</span>
              </button>
            ))}
          </div>
        </aside>

        {/* Main Workspace Area */}
        <main className="flex-1 bg-[#0c0e10] relative overflow-hidden">
          {/* Background Atmosphere */}
          <div className="absolute inset-0 z-0 pointer-events-none">
            <div className="absolute inset-0 bg-gradient-to-tr from-[#0c0e10] via-[#171a1c] to-[#0c0e10] opacity-60" />
            <div className="absolute top-1/4 left-1/4 w-[500px] h-[500px] bg-[#00D4FF]/5 blur-[120px] rounded-full" />
            <div className="absolute bottom-1/4 right-1/4 w-[500px] h-[500px] bg-[#ff51fa]/5 blur-[120px] rounded-full" />
          </div>

          {/* Draggable Regions Container */}
          <div className="absolute inset-0 z-10">
            
            {/* Region 01: Main Content Region */}
            <Rnd
              size={{ width: regions.mainContent.width, height: regions.mainContent.height }}
              position={{ x: regions.mainContent.x, y: regions.mainContent.y }}
              onDragStop={(e, d) => updateRegion('mainContent', { x: d.x, y: d.y })}
              onResizeStop={(e, direction, ref, delta, position) => {
                updateRegion('mainContent', {
                  width: parseInt(ref.style.width),
                  height: parseInt(ref.style.height),
                  ...position,
                });
              }}
              bounds="parent"
              className="z-20"
            >
              <div className="w-full h-full bg-[#171a1c]/30 backdrop-blur-md rounded-[2rem] border border-white/5 flex items-center justify-center relative group overflow-hidden">
                <div className="absolute top-6 left-8 bg-[#00D4FF]/10 border border-[#00D4FF]/30 px-3 py-1 rounded text-[9px] font-bold text-[#00D4FF] uppercase tracking-tighter cursor-move">
                  Region 01: Main Content Region
                </div>
                <div className="text-center opacity-40 group-hover:opacity-100 transition-opacity">
                  <p className="font-headline text-xs text-primary font-bold tracking-[0.5em] uppercase mb-2">Active Workspace</p>
                  <p className="text-slate-500 text-[10px] uppercase tracking-widest">Main Text / Fig Region</p>
                </div>
              </div>
            </Rnd>

            {/* Region 02: Character Chat Layer */}
            <Rnd
              size={{ width: regions.chatLayer.width, height: regions.chatLayer.height }}
              position={{ x: regions.chatLayer.x, y: regions.chatLayer.y }}
              onDragStop={(e, d) => updateRegion('chatLayer', { x: d.x, y: d.y })}
              onResizeStop={(e, direction, ref, delta, position) => {
                updateRegion('chatLayer', {
                  width: parseInt(ref.style.width),
                  height: parseInt(ref.style.height),
                  ...position,
                });
              }}
              bounds="parent"
              className="z-30"
            >
              <div className="w-full h-full bg-[#171a1c]/60 backdrop-blur-2xl p-6 rounded-[2rem] border border-white/5 shadow-2xl relative overflow-hidden flex flex-col">
                <div className="absolute -top-24 -right-24 w-48 h-48 bg-[#00D4FF]/5 blur-[80px]" />
                <div className="absolute top-6 right-8 bg-[#ff51fa]/10 border border-[#ff51fa]/30 px-3 py-1 rounded text-[9px] font-bold text-[#ff51fa] uppercase tracking-tighter cursor-move">
                  Region 02: Character Chat Layer
                </div>
                
                <div className="flex items-start gap-4 relative z-10 h-full overflow-hidden">
                  <div className="flex-shrink-0">
                    <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-[#00D4FF] to-[#00687e] flex items-center justify-center shadow-lg shadow-[#00D4FF]/20">
                      <MessageSquare size={20} className="text-white" fill="currentColor" />
                    </div>
                  </div>
                  
                  <div className="flex-1 flex flex-col h-full">
                    <div className="flex items-center gap-3 mb-2">
                      <span className="text-[10px] font-black text-[#00D4FF] uppercase tracking-widest">Emma</span>
                      <div className="h-[1px] w-6 bg-white/10" />
                      <span className="text-[8px] font-bold text-slate-500 uppercase tracking-widest">Dialogue Node #422</span>
                    </div>
                    
                    {/* Dialogue Font Size Reduced (0.5x of 2xl is roughly base/sm) */}
                    <h3 className="text-sm font-medium text-white leading-relaxed flex-1 overflow-y-auto pr-2">
                      "If we process the dimensional shift now, the narrative integrity might fracture. Are you sure about this, <span className="text-[#00D4FF] underline underline-offset-4 decoration-2">Hiro</span>?"
                    </h3>
                    
                    <div className="mt-4 pt-4 border-t border-white/5 flex gap-6">
                      <div>
                        <p className="text-[8px] uppercase font-bold text-slate-500 tracking-tighter mb-1">Caption Layer</p>
                        <p className="text-[10px] text-slate-400 font-mono">FR: "Si nous traitons le décalage dimensionnel..."</p>
                      </div>
                      <div>
                        <p className="text-[8px] uppercase font-bold text-slate-500 tracking-tighter mb-1">Voice Metadata</p>
                        <p className="text-[10px] text-[#00D4FF] font-mono">EMMA_V4_EMOTIVE_B.wav [03.2s]</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </Rnd>

            {/* Region 03: Function Region */}
            <Rnd
              size={{ width: regions.functionRegion.width, height: regions.functionRegion.height }}
              position={{ x: regions.functionRegion.x, y: regions.functionRegion.y }}
              onDragStop={(e, d) => updateRegion('functionRegion', { x: d.x, y: d.y })}
              onResizeStop={(e, direction, ref, delta, position) => {
                updateRegion('functionRegion', {
                  width: parseInt(ref.style.width),
                  height: parseInt(ref.style.height),
                  ...position,
                });
              }}
              bounds="parent"
              className="z-40"
            >
              <div className="w-full h-full bg-[#171a1c]/80 backdrop-blur-xl p-4 rounded-2xl border border-white/5 shadow-xl flex flex-col gap-3">
                <div className="flex justify-between items-center">
                  <div className="text-left">
                    <h2 className="text-xs font-bold text-white tracking-tight">Function Region</h2>
                    <p className="text-[7px] uppercase tracking-[0.2em] text-[#00D4FF] font-bold">AI Control Interface</p>
                  </div>
                  <div className="bg-[#00D4FF]/10 border border-[#00D4FF]/30 px-2 py-0.5 rounded text-[7px] font-bold text-[#00D4FF] uppercase tracking-tighter cursor-move">
                    Region 03
                  </div>
                </div>
                
                <div className="flex gap-2 flex-1">
                  {[RefreshCw, Play, ChevronRight, ChevronLeft, Settings].map((Icon, i) => (
                    <button key={i} className="flex-1 bg-[#232629] rounded-lg flex items-center justify-center text-slate-400 hover:text-[#00D4FF] transition-colors border border-white/5">
                      <Icon size={16} />
                    </button>
                  ))}
                </div>
              </div>
            </Rnd>

            {/* Timeline Region */}
            <Rnd
              size={{ width: regions.timelineRegion.width, height: regions.timelineRegion.height }}
              position={{ x: regions.timelineRegion.x, y: regions.timelineRegion.y }}
              onDragStop={(e, d) => updateRegion('timelineRegion', { x: d.x, y: d.y })}
              onResizeStop={(e, direction, ref, delta, position) => {
                updateRegion('timelineRegion', {
                  width: parseInt(ref.style.width),
                  height: parseInt(ref.style.height),
                  ...position,
                });
              }}
              bounds="parent"
              className="z-40"
            >
              <div className="w-full h-full bg-[#171a1c]/80 backdrop-blur-xl p-4 rounded-2xl border border-white/5 shadow-xl flex flex-col justify-center">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-[8px] font-bold text-slate-400 uppercase tracking-widest cursor-move">Sequence: 024</span>
                  <span className="text-[8px] font-bold text-[#00D4FF]">00:42 / 01:15</span>
                </div>
                <div className="h-1 w-full bg-[#0c0e10] rounded-full overflow-hidden relative">
                  <div className="absolute top-0 left-0 h-full w-[60%] bg-gradient-to-r from-[#00D4FF] to-[#00687e]" />
                  <div className="absolute top-0 left-[60%] -translate-x-1/2 h-full w-1 bg-[#ff51fa] shadow-[0_0_10px_#ff51fa]" />
                </div>
                <div className="flex gap-1 mt-2">
                  <div className="h-2 w-10 bg-[#00D4FF]/20 rounded-sm" />
                  <div className="h-2 w-16 bg-[#00D4FF]/40 rounded-sm" />
                  <div className="h-2 w-6 bg-[#ff51fa]/30 rounded-sm border-l-2 border-[#ff51fa]" />
                  <div className="h-2 flex-1 bg-[#232629] rounded-sm" />
                </div>
              </div>
            </Rnd>

            {/* Character Fig Region */}
            <Rnd
              size={{ width: regions.characterFigRegion.width, height: regions.characterFigRegion.height }}
              position={{ x: regions.characterFigRegion.x, y: regions.characterFigRegion.y }}
              onDragStop={(e, d) => updateRegion('characterFigRegion', { x: d.x, y: d.y })}
              onResizeStop={(e, direction, ref, delta, position) => {
                updateRegion('characterFigRegion', {
                  width: parseInt(ref.style.width),
                  height: parseInt(ref.style.height),
                  ...position,
                });
              }}
              bounds="parent"
              className="z-50"
            >
              <div className="w-full h-full bg-[#171a1c]/40 backdrop-blur-md rounded-[2rem] border border-white/5 p-4 flex items-end justify-center gap-2 relative overflow-hidden">
                <div className="absolute top-4 left-1/2 -translate-x-1/2 bg-white/5 px-3 py-1 rounded-full border border-white/10 backdrop-blur-md cursor-move z-10">
                  <span className="text-[8px] font-bold text-slate-400 tracking-widest uppercase">Character Fig Region</span>
                </div>
                
                {/* Emma Figure */}
                <div className="relative flex-1 h-[80%] flex flex-col justify-end">
                  <div className="text-center mb-1">
                    <span className="text-[8px] font-bold text-[#00D4FF] uppercase tracking-tighter">Emma</span>
                  </div>
                  <div className="relative h-full w-full">
                    <img 
                      src={EMMA_IMG} 
                      alt="Emma" 
                      className="h-full w-full object-contain drop-shadow-[0_0_15px_rgba(0,212,255,0.15)]"
                      referrerPolicy="no-referrer"
                    />
                  </div>
                </div>

                {/* Hiro Figure */}
                <div className="relative flex-1 h-[80%] flex flex-col justify-end">
                  <div className="text-center mb-1">
                    <span className="text-[8px] font-bold text-[#ff51fa] uppercase tracking-tighter">Hiro</span>
                  </div>
                  <div className="relative h-full w-full">
                    <img 
                      src={HIRO_IMG} 
                      alt="Hiro" 
                      className="h-full w-full object-contain drop-shadow-[0_0_15px_rgba(255,81,250,0.15)] grayscale contrast-125"
                      referrerPolicy="no-referrer"
                    />
                  </div>
                </div>
              </div>
            </Rnd>

          </div>
        </main>
      </div>

      {/* Bottom Navigation Bar */}
      <footer className="h-16 border-t border-white/5 bg-[#0c0e10] flex items-center justify-center gap-8 z-50">
        {[
          { id: 'Timeline', icon: Clock, label: 'Timeline', active: true },
          { id: 'Character', icon: Users, label: 'Character' },
          { id: 'Script', icon: FileText, label: 'Script' },
          { id: 'Export', icon: Share2, label: 'Export' },
        ].map((item) => (
          <button
            key={item.id}
            className={`flex flex-col items-center justify-center px-6 py-1.5 rounded-xl transition-all ${
              item.active 
                ? 'text-[#ff51fa] bg-[#ff51fa]/10 border border-[#ff51fa]/20' 
                : 'text-slate-500 hover:text-white hover:bg-white/5'
            }`}
          >
            <item.icon size={18} />
            <span className="text-[9px] font-bold uppercase mt-1 tracking-wider">{item.label}</span>
          </button>
        ))}
      </footer>
    </div>
  );
}
