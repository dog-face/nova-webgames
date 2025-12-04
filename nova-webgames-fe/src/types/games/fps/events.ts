import type { Vector3 } from '../../../utils/games/fps/math';
import type { EnemyAI } from '../../../utils/games/fps/enemyAI';

/**
 * Event type definitions for FPS game events
 */

export enum FPSGameEvent {
  ENEMY_SPAWNED = 'ENEMY_SPAWNED',
  ENEMY_DIED = 'ENEMY_DIED',
  PLAYER_HIT = 'PLAYER_HIT',
  WEAPON_FIRED = 'WEAPON_FIRED',
  SCORE_CHANGED = 'SCORE_CHANGED',
  GAME_STATE_CHANGED = 'GAME_STATE_CHANGED',
  AMMO_CHANGED = 'AMMO_CHANGED',
  RELOAD_STARTED = 'RELOAD_STARTED',
  RELOAD_COMPLETED = 'RELOAD_COMPLETED',
}

export interface EnemySpawnedEvent {
  enemy: EnemyAI;
  position: Vector3;
}

export interface EnemyDiedEvent {
  enemyId: string;
  position: Vector3;
  score: number;
}

export interface PlayerHitEvent {
  damage: number;
  newHealth: number;
  attackerId?: string;
}

export interface WeaponFiredEvent {
  position: Vector3;
  direction: Vector3;
  hit: boolean;
  hitTarget?: string;
}

export interface ScoreChangedEvent {
  score: number;
  delta: number;
  reason: 'kill' | 'hit' | 'other';
}

export interface GameStateChangedEvent {
  state: 'menu' | 'playing' | 'paused' | 'gameover';
}

export interface AmmoChangedEvent {
  ammo: number;
  maxAmmo: number;
  delta: number;
}

export interface ReloadEvent {
  duration: number;
}

