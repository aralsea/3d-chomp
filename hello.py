
def legal_moves(state):
    """
    state: frozenset of (x, y, z) のタプルで表される状態
    (0,0,0) は毒ブロックで、取り除く手は不合法
    選んだブロック (i,j,k) に対して、x>=i, y>=j, z>=k となるブロック群を取り除く。
    """
    moves = []
    for cube in state:
        if cube == (0, 0, 0):
            continue  # 毒ブロックは選べない
        # この手で取り除かれるブロックの集合
        remove = {c for c in state if c[0] >= cube[0] and c[1] >= cube[1] and c[2] >= cube[2]}
        # もし毒ブロックが取り除かれてしまうなら不合法
        if (0, 0, 0) in remove:
            continue
        new_state = frozenset(state - remove)
        moves.append((cube, new_state))
    return moves

# 状態ごとの勝敗をメモ化する辞書
cache = {}

def win(state):
    """
    state が与えられたとき、現在の手番のプレイヤーが勝てるかどうかを返す。
    終端状態として、状態が {(0,0,0)} のみの場合は負け（すなわち必勝手が存在しない）。
    """
    # 終端状態: 盤面に毒ブロックのみ残っているなら、手番のプレイヤーは負け
    if state == frozenset({(0, 0, 0)}):
        return False
    if state in cache:
        return cache[state]
    moves = legal_moves(state)
    if not moves:
        cache[state] = False
        return False
    # どれかの合法手で相手が負けになるなら、現在の状態は勝ち
    for move, new_state in moves:
        if not win(new_state):
            cache[state] = True
            return True
    cache[state] = False
    return False

def winning_moves(state):
    """
    現在の状態から、勝ちにつながる（必勝となる）一手を返す。
    見つからなければ None を返す。
    """
    moves = []
    for move, new_state in legal_moves(state):
        if not win(new_state):
            moves.append(move)
    return moves

# 初期状態: 全ての N*N*N のブロックが揃っている
N = 5
initial_state = frozenset((x, y, z) for x in range(N) for y in range(N) for z in range(N))

# 初期状態が先手必勝かどうか
first_win = win(initial_state)
moves = winning_moves(initial_state)
print("初期状態は先手必勝か:", first_win)
print("先手の必勝手")
for move in moves:
    print(move)
