import { describe, it, expect } from 'vitest';
import { GAME_CONFIG } from '../constants';

describe('Combat Calculations', () => {
  describe('Weapon Configuration', () => {
    it('should have valid weapon range', () => {
      expect(GAME_CONFIG.WEAPON_RANGE).toBeGreaterThan(0);
      expect(GAME_CONFIG.WEAPON_RANGE).toBe(100);
    });
    
    it('should have valid weapon damage', () => {
      expect(GAME_CONFIG.WEAPON_DAMAGE).toBeGreaterThan(0);
      expect(GAME_CONFIG.WEAPON_DAMAGE).toBe(25);
    });
    
    it('should have valid fire rate', () => {
      expect(GAME_CONFIG.WEAPON_FIRE_RATE).toBeGreaterThan(0);
      expect(GAME_CONFIG.WEAPON_FIRE_RATE).toBe(10);
    });
  });
  
  describe('Enemy Configuration', () => {
    it('should have valid enemy health', () => {
      expect(GAME_CONFIG.ENEMY_HEALTH).toBeGreaterThan(0);
      expect(GAME_CONFIG.ENEMY_HEALTH).toBe(50);
    });
    
    it('should have valid enemy damage', () => {
      expect(GAME_CONFIG.ENEMY_DAMAGE).toBeGreaterThan(0);
      expect(GAME_CONFIG.ENEMY_DAMAGE).toBe(10);
    });
    
    it('should calculate shots to kill enemy', () => {
      const shotsToKill = Math.ceil(GAME_CONFIG.ENEMY_HEALTH / GAME_CONFIG.WEAPON_DAMAGE);
      expect(shotsToKill).toBe(2); // 50 health / 25 damage = 2 shots
    });
  });
  
  describe('Damage Calculations', () => {
    it('should calculate damage correctly', () => {
      const enemyHealth = GAME_CONFIG.ENEMY_HEALTH;
      const damage = GAME_CONFIG.WEAPON_DAMAGE;
      const remainingHealth = enemyHealth - damage;
      
      expect(remainingHealth).toBe(25);
    });
    
    it('should not allow negative health', () => {
      const enemyHealth = 10;
      const damage = GAME_CONFIG.WEAPON_DAMAGE;
      const remainingHealth = Math.max(0, enemyHealth - damage);
      
      expect(remainingHealth).toBe(0);
    });
  });
});

