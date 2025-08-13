import random
import time
from enum import Enum
from typing import Dict, List, Optional, Tuple

"""
Consensus Basics (Raft-style leader election simulation, simplified)

This module provides a minimal, synchronous simulation of leader election inspired by Raft:
  - Nodes are either Follower, Candidate, or Leader
  - Time proceeds in discrete ticks (no threads), with randomized election timeouts
  - If a follower doesn't hear from a leader within its timeout, it becomes a candidate
  - Candidate increments term, votes for self, requests votes; majority wins becomes leader
  - Leader sends heartbeats to reset followers' timeouts

This is a teaching/demonstration tool and intentionally omits:
  - Persistent log/state, log replication, commit indices
  - Real RPC and timing, network partitions, randomized delays
  - Split votes resolution beyond retrying in new terms
"""

class Role(Enum):
    FOLLOWER = "Follower"
    CANDIDATE = "Candidate"
    LEADER = "Leader"

class Node:
    def __init__(self, node_id: int, peers: List[int], rng: random.Random):
        self.id = node_id
        self.peers = peers
        self.rng = rng

        self.role = Role.FOLLOWER
        self.current_term = 0
        self.voted_for: Optional[int] = None
        self.last_heartbeat_tick = 0

        # Election timeout randomized range (ticks)
        self.timeout_min = 5
        self.timeout_max = 10
        self.election_timeout = self._random_timeout()

    def _random_timeout(self) -> int:
        return self.rng.randint(self.timeout_min, self.timeout_max)

    def reset_election_timer(self, tick: int):
        self.last_heartbeat_tick = tick
        self.election_timeout = self._random_timeout()

    def time_since_heartbeat(self, tick: int) -> int:
        return tick - self.last_heartbeat_tick

    def __repr__(self):
        return f"Node(id={self.id}, term={self.current_term}, role={self.role.value})"

class Cluster:
    def __init__(self, n: int, seed: int = 42):
        self.rng = random.Random(seed)
        self.nodes: Dict[int, Node] = {}
        ids = list(range(n))
        for i in ids:
            peers = [p for p in ids if p != i]
            self.nodes[i] = Node(i, peers, self.rng)
        # Initialize all followers and reset timers
        self.tick = 0
        for node in self.nodes.values():
            node.role = Role.FOLLOWER
            node.current_term = 0
            node.voted_for = None
            node.reset_election_timer(self.tick)

    def leader(self) -> Optional[int]:
        leaders = [nid for nid, n in self.nodes.items() if n.role == Role.LEADER]
        if len(leaders) == 1:
            return leaders[0]
        return None

    def step(self) -> None:
        """
        One synchronous tick:
          - Leaders send heartbeat
          - Followers/Candidates check timeouts and possibly start elections
          - Candidates request votes; majority wins
        """
        self.tick += 1
        events: List[str] = []

        # Leaders send heartbeats
        leader_id = self.leader()
        if leader_id is not None:
            leader = self.nodes[leader_id]
            # Heartbeat resets followers' timers
            for nid, node in self.nodes.items():
                if nid == leader_id:
                    continue
                node.reset_election_timer(self.tick)
            events.append(f"[t={self.tick}] Leader {leader_id} (term {leader.current_term}) sent heartbeats")

        # Followers/Candidates check timeouts
        to_start_election: List[int] = []
        for nid, node in self.nodes.items():
            if node.role == Role.LEADER:
                continue
            if node.time_since_heartbeat(self.tick) >= node.election_timeout:
                to_start_election.append(nid)

        # Start elections (synchronously, one by one to keep it simple)
        for nid in to_start_election:
            node = self.nodes[nid]
            # Become candidate
            node.role = Role.CANDIDATE
            node.current_term += 1
            node.voted_for = nid
            node.reset_election_timer(self.tick)
            term = node.current_term
            votes = 1  # self-vote
            # Request votes
            for pid in node.peers:
                peer = self.nodes[pid]
                # Grant vote if peer hasn't voted in this term or voted for candidate, and candidate's term is >=
                if peer.current_term < term:
                    # Update peer term if behind (Raft: step-down)
                    peer.current_term = term
                    peer.role = Role.FOLLOWER
                    peer.voted_for = None
                if peer.voted_for is None and peer.current_term == term:
                    peer.voted_for = nid
                    votes += 1
            events.append(f"[t={self.tick}] Node {nid} started election for term {term}, votes={votes}")

            # Majority?
            if votes > len(self.nodes) // 2:
                # This candidate becomes leader; others step down if same term
                node.role = Role.LEADER
                for pid, peer in self.nodes.items():
                    if pid == nid:
                        continue
                    if peer.current_term == term and peer.role != Role.FOLLOWER:
                        peer.role = Role.FOLLOWER
                events.append(f"[t={self.tick}] Node {nid} became LEADER for term {term}")
            else:
                # Stay candidate; will retry after another timeout
                events.append(f"[t={self.tick}] Node {nid} failed to get majority (votes={votes})")

        # Print events for this tick
        for e in events:
            print(e)

    def run(self, max_ticks: int = 50) -> None:
        """
        Run until a stable leader is elected and heartbeats are seen,
        or until max_ticks to limit demo length.
        """
        print("Initial cluster state:")
        for nid, node in self.nodes.items():
            print(f"  {node}")
        print()

        last_leader: Optional[int] = None
        stable_ticks = 0
        while self.tick < max_ticks:
            self.step()
            cur_leader = self.leader()
            # Track stability: same leader for several ticks with heartbeats
            if cur_leader is not None and cur_leader == last_leader:
                stable_ticks += 1
            else:
                stable_ticks = 0
                last_leader = cur_leader
            if stable_ticks >= 5:
                break

        print("\nFinal cluster state:")
        for nid, node in self.nodes.items():
            print(f"  {node}")


def demo():
    print("Consensus Basics (Raft-style Leader Election) Demo")
    print("=" * 55)
    cluster = Cluster(n=5, seed=7)
    cluster.run(max_ticks=60)
    print("\nNotes & Interview Tips:")
    print("  - Raft splits consensus into leader election, log replication, and safety.")
    print("  - Randomized election timeouts reduce split votes.")
    print("  - Real systems handle persistent logs, RPC timeouts, retries, and partitions.")
    print("  - Paxos follows different mechanics (proposers/acceptors/learners) with quorums.")


if __name__ == "__main__":
    demo()
