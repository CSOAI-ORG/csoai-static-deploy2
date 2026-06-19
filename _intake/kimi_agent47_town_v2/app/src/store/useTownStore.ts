import { create } from 'zustand';
import type { GameStore } from '@/types';

export const useTownStore = create<GameStore>((set) => ({
  // Time
  gameTime: 8 * 3600, // Start at 8:00 AM
  timeScale: 60,
  day: 1,
  timeOfDay: 8,

  // Camera
  cameraMode: 'isometric',
  cameraTarget: [0, 0, 0],

  // Selected
  selectedAgentId: null,
  selectedBuildingId: null,

  // UI Panels
  activePanels: ['minimap', 'agentList', 'controlBar', 'notifications'],
  modalOpen: null,

  // Settings
  showPheromones: true,
  showAgentNames: true,
  showBuildingLabels: true,
  graphicsQuality: 'medium',
  soundEnabled: false,
  musicVolume: 0.5,
  sfxVolume: 0.5,

  // Weather
  weather: 'clear',

  // Economy
  totalTransactions: 0,
  activeProposals: 0,

  // Simulation
  isPaused: false,
  simulationSpeed: 1,

  // Actions
  setTimeOfDay: (hour) => set({ timeOfDay: hour }),
  advanceTime: (delta) =>
    set((state) => {
      const newGameTime = state.gameTime + delta * state.timeScale * state.simulationSpeed;
      const day = Math.floor(newGameTime / 86400) + 1;
      const timeOfDay = (newGameTime % 86400) / 3600;
      return { gameTime: newGameTime, day, timeOfDay };
    }),
  setCameraMode: (mode) => set({ cameraMode: mode }),
  setCameraTarget: (target) => set({ cameraTarget: target }),
  selectAgent: (id) => set({ selectedAgentId: id }),
  selectBuilding: (id) => set({ selectedBuildingId: id }),
  togglePanel: (panel) =>
    set((state) => ({
      activePanels: state.activePanels.includes(panel)
        ? state.activePanels.filter((p) => p !== panel)
        : [...state.activePanels, panel],
    })),
  openModal: (modal) => set({ modalOpen: modal }),
  setShowPheromones: (show) => set({ showPheromones: show }),
  setShowAgentNames: (show) => set({ showAgentNames: show }),
  setShowBuildingLabels: (show) => set({ showBuildingLabels: show }),
  setWeather: (weather) => set({ weather }),
  setPaused: (paused) => set({ isPaused: paused }),
  setSimulationSpeed: (speed) => set({ simulationSpeed: speed }),
  togglePaused: () => set((state) => ({ isPaused: !state.isPaused })),
}));
