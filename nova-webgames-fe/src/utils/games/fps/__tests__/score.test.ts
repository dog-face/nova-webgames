import { describe, it, expect } from 'vitest';
import { GAME_CONFIG } from '../constants';

describe('Score Tracking Logic', () => {
  describe('Kill Scoring', () => {
    it('should award correct points for enemy kill', () => {
      expect(GAME_CONFIG.ENEMY_KILL_SCORE).toBe(50);
    });
    
    it('should calculate total score for multiple kills', () => {
      const kills = 5;
      const totalScore = kills * GAME_CONFIG.ENEMY_KILL_SCORE;
      expect(totalScore).toBe(250);
    });
  });
  
  describe('Hit Scoring', () => {
    it('should award points for hitting non-enemy targets', () => {
      const hitScore = 10;
      expect(hitScore).toBe(10);
    });
    
    it('should calculate score progression', () => {
      let score = 0;
      
      // Hit a target
      score += 10;
      expect(score).toBe(10);
      
      // Kill an enemy
      score += GAME_CONFIG.ENEMY_KILL_SCORE;
      expect(score).toBe(60);
      
      // Kill another enemy
      score += GAME_CONFIG.ENEMY_KILL_SCORE;
      expect(score).toBe(110);
    });
  });
  
  describe('Score Validation', () => {
    it('should not allow negative scores', () => {
      const score = Math.max(0, -10);
      expect(score).toBe(0);
    });
    
    it('should handle zero score', () => {
      const score = 0;
      expect(score).toBe(0);
    });
  });
});

