import { describe, it, expect, beforeEach, vi } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { useFPSCombat } from '../useFPSCombat';
import { GAME_CONFIG } from '../../../../utils/games/fps/constants';
import { EnemyAI } from '../../../../utils/games/fps/enemyAI';
import * as THREE from 'three';

// Mock AudioManager
const mockAudioManager = {
  playSound: vi.fn(),
  setMasterVolume: vi.fn(),
  setSFXVolume: vi.fn(),
  setMusicVolume: vi.fn(),
  mute: vi.fn(),
  unmute: vi.fn(),
  cleanup: vi.fn(),
};

// Mock enemies ref
const createMockEnemiesRef = () => {
  const enemies = new Map<string, EnemyAI>();
  const enemy = new EnemyAI('enemy-1', [0, 1, 5]);
  enemies.set('enemy-1', enemy);
  return { current: enemies } as React.MutableRefObject<Map<string, EnemyAI>>;
};

describe('useFPSCombat', () => {
  let enemiesRef: React.MutableRefObject<Map<string, EnemyAI>>;
  let setGameState: ReturnType<typeof vi.fn>;
  
  beforeEach(() => {
    enemiesRef = createMockEnemiesRef();
    setGameState = vi.fn((updater) => {
      if (typeof updater === 'function') {
        const prevState = {
          player: { position: [0, 2, 0], rotation: [0, 0, 0], health: 100, armor: 0 },
          enemies: [],
          projectiles: [],
          score: 0,
          kills: 0,
          deaths: 0,
        };
        return updater(prevState);
      }
      return updater;
    });
    vi.clearAllMocks();
  });
  
  it('should initialize with default combat state', () => {
    const { result } = renderHook(() =>
      useFPSCombat(
        mockAudioManager as any,
        enemiesRef,
        setGameState,
        () => null,
        () => [0, 2, 0],
        () => [0, 0, -1]
      )
    );
    
    expect(result.current.ammo).toBe(30);
    expect(result.current.maxAmmo).toBe(30);
    expect(result.current.reloadTime).toBe(0);
  });
  
  it('should handle shooting and decrement ammo', () => {
    const { result } = renderHook(() =>
      useFPSCombat(
        mockAudioManager as any,
        enemiesRef,
        setGameState,
        () => null,
        () => [0, 2, 0],
        () => [0, 0, -1]
      )
    );
    
    const currentTime = performance.now();
    act(() => {
      result.current.handleShoot({ shoot: true }, currentTime);
    });
    
    expect(result.current.ammo).toBe(29);
    expect(mockAudioManager.playSound).toHaveBeenCalled();
  });
  
  it('should handle reload', () => {
    const { result } = renderHook(() =>
      useFPSCombat(
        mockAudioManager as any,
        enemiesRef,
        setGameState,
        () => null,
        () => [0, 2, 0],
        () => [0, 0, -1]
      )
    );
    
    // Set ammo to 0
    act(() => {
      result.current.handleShoot({ shoot: true }, performance.now());
    });
    
    // Trigger reload
    act(() => {
      result.current.handleReload({ reload: true });
    });
    
    expect(result.current.reloadTime).toBe(2000);
    expect(mockAudioManager.playSound).toHaveBeenCalled();
  });
  
  it('should reset combat state', () => {
    const { result } = renderHook(() =>
      useFPSCombat(
        mockAudioManager as any,
        enemiesRef,
        setGameState,
        () => null,
        () => [0, 2, 0],
        () => [0, 0, -1]
      )
    );
    
    // Modify state
    act(() => {
      result.current.handleShoot({ shoot: true }, performance.now());
    });
    
    expect(result.current.ammo).toBe(29);
    
    // Reset
    act(() => {
      result.current.resetCombat();
    });
    
    expect(result.current.ammo).toBe(30);
    expect(result.current.reloadTime).toBe(0);
  });
});

