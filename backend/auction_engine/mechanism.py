from typing import List, Dict
import copy

class AuctionMechanism:
    def run(self, candidates: List[Dict]) -> List[Dict]:
        """
        Run the auction mechanism.
        candidates: List of dicts, each containing 'bid', 'pctr', 'ad_id', etc.
        Returns: List of dicts with added 'rank', 'cost', 'surplus'.
        """
        raise NotImplementedError

class GSP(AuctionMechanism):
    """
    Generalized Second Price Auction.
    Rank by Bid * pCTR (eCPM).
    Payment = Next Highest Score / Own pCTR.
    """
    def run(self, candidates: List[Dict]) -> List[Dict]:
        candidates = copy.deepcopy(candidates)
        # 1. Calculate Score (eCPM)
        for c in candidates:
            c['score'] = c['bid'] * c['pctr']
        
        # 2. Sort by Score descending
        candidates.sort(key=lambda x: x['score'], reverse=True)
        
        # 3. Calculate Payment
        for i in range(len(candidates)):
            candidates[i]['rank'] = i + 1
            if i < len(candidates) - 1:
                next_score = candidates[i+1]['score']
                # Cost per click = Next Score / Own pCTR
                # Avoid division by zero
                pctr = candidates[i]['pctr'] if candidates[i]['pctr'] > 1e-6 else 1e-6
                candidates[i]['cost'] = next_score / pctr
            else:
                # Last one pays reserve price (simplified to 0.01 or some small value)
                candidates[i]['cost'] = 0.01
            
            # Ensure cost doesn't exceed bid (Rationality constraint)
            # In GSP, cost is usually <= bid if truthful, but we clamp it just in case.
            candidates[i]['cost'] = min(candidates[i]['cost'], candidates[i]['bid'])
            
            # Consumer Surplus = Value (Bid) - Cost
            # Assuming Bid represents true value for simplicity in surplus calc, 
            # though in GSP truthful bidding is not always dominant strategy.
            candidates[i]['surplus'] = candidates[i]['bid'] - candidates[i]['cost']
            
        return candidates

class VCG(AuctionMechanism):
    """
    Vickrey-Clarke-Groves Auction.
    Truthful mechanism.
    Payment = Externality imposed on others.
    """
    def run(self, candidates: List[Dict]) -> List[Dict]:
        candidates = copy.deepcopy(candidates)
        # 1. Calculate Score
        for c in candidates:
            c['score'] = c['bid'] * c['pctr']
            
        # 2. Sort by Score descending (Allocation)
        candidates.sort(key=lambda x: x['score'], reverse=True)
        
        # 3. Calculate Payment
        # For VCG in ad auctions (multi-slot), it's complex.
        # Simplified Scenario: Single Slot Auction (equivalent to Second Price)
        # If Multi-Slot with position bias:
        #   Social Welfare of others if i participates vs if i doesn't.
        # Let's assume Single Slot for simplicity of the Demo first, 
        # OR assume position discounts (v_j * CTR_pos).
        
        # Let's implement a simplified VCG for single slot first, which is just 2nd price.
        # But to make it distinct from GSP in a multi-slot demo, we need position effects.
        # Let's assume Position CTR drop-offs: Pos 1: 1.0, Pos 2: 0.8, Pos 3: 0.5...
        
        position_weights = [1.0, 0.8, 0.5, 0.3, 0.1] # CTR discount factors for positions
        
        # Re-calculate "Value" to the platform (Total Expected Revenue? No, Social Welfare is sum of valuations)
        # Valuation of advertiser i for position k = Bid_i * pCTR_i * PosWeight_k
        
        # Allocation is already done by sorting Bid*pCTR (assuming position weights are separable and monotonic)
        
        for i in range(len(candidates)):
            candidates[i]['rank'] = i + 1
            
            # Calculate payment for candidate i at position i
            # Payment_i = (SW_{-i} without i) - (SW_{-i} with i)
            
            # SW_{-i} with i: Sum of values of other candidates j!=i in their assigned positions
            sw_with_i = 0
            for j in range(len(candidates)):
                if i == j: continue
                pos_idx = j # If i is present, j takes rank j (0-indexed)
                if pos_idx < len(position_weights):
                    sw_with_i += candidates[j]['bid'] * candidates[j]['pctr'] * position_weights[pos_idx]
            
            # SW_{-i} without i: Re-run allocation without i
            others = [c for idx, c in enumerate(candidates) if idx != i]
            # Others are already sorted by Bid*pCTR
            sw_without_i = 0
            for j in range(len(others)):
                pos_idx = j # j takes rank j
                if pos_idx < len(position_weights):
                    sw_without_i += others[j]['bid'] * others[j]['pctr'] * position_weights[pos_idx]
            
            # Payment (Total expected payment)
            total_payment = sw_without_i - sw_with_i
            
            # Cost per click (CPC)
            # Total Payment = CPC * Expected Clicks
            # Expected Clicks = pCTR_i * PosWeight_i
            pos_weight = position_weights[i] if i < len(position_weights) else 0
            expected_clicks = candidates[i]['pctr'] * pos_weight
            
            if expected_clicks > 1e-6:
                candidates[i]['cost'] = total_payment / expected_clicks
            else:
                candidates[i]['cost'] = 0
                
            candidates[i]['cost'] = max(0, candidates[i]['cost']) # No negative payments
            candidates[i]['surplus'] = candidates[i]['bid'] - candidates[i]['cost']

        return candidates
