"""
Minimum Window Substring - LeetCode Problem

Given two strings s and t of lengths m and n respectively, return the minimum window 
substring of s such that every character in t (including duplicates) is included in the window. 
If there is no such window, return the empty string "".

The testcases will be generated such that the answer is unique.
"""

from collections import Counter, defaultdict
from .._registry import register_problem
from .._runner import TestCase, run_test_cases, create_demo_output
from .._types import Category, Difficulty


class Solution:
    def minWindow(self, s: str, t: str) -> str:
        """
        Find minimum window substring using sliding window with character counting.
        
        Time Complexity: O(|s| + |t|) - each character in s visited at most twice
        Space Complexity: O(|s| + |t|) - for character frequency maps
        
        Args:
            s: Source string to search in
            t: Target string containing required characters
            
        Returns:
            str: Minimum window substring containing all characters of t
        """
        if not s or not t or len(t) > len(s):
            return ""
        
        # Count required characters
        t_count = Counter(t)
        required_chars = len(t_count)
        
        # Sliding window variables
        left = 0
        formed_chars = 0  # Number of unique chars in current window with desired frequency
        window_counts = defaultdict(int)
        
        # Result tracking
        min_len = float('inf')
        min_left = 0
        
        for right in range(len(s)):
            # Add character to window
            char = s[right]
            window_counts[char] += 1
            
            # Check if frequency of current character matches desired count
            if char in t_count and window_counts[char] == t_count[char]:
                formed_chars += 1
            
            # Try to shrink window from left
            while formed_chars == required_chars:
                # Update result if this window is smaller
                if right - left + 1 < min_len:
                    min_len = right - left + 1
                    min_left = left
                
                # Remove leftmost character
                left_char = s[left]
                window_counts[left_char] -= 1
                if left_char in t_count and window_counts[left_char] < t_count[left_char]:
                    formed_chars -= 1
                
                left += 1
        
        return "" if min_len == float('inf') else s[min_left:min_left + min_len]
    
    def minWindowBruteForce(self, s: str, t: str) -> str:
        """
        Brute force approach checking all possible substrings (not optimal).
        
        Time Complexity: O(|s|² * |t|) - for each substring, check if it contains all chars of t
        Space Complexity: O(|t|) - for character counting
        """
        if not s or not t or len(t) > len(s):
            return ""
        
        t_count = Counter(t)
        min_window = ""
        min_len = float('inf')
        
        for i in range(len(s)):
            for j in range(i, len(s)):
                window = s[i:j+1]
                window_count = Counter(window)
                
                # Check if window contains all characters of t
                valid = True
                for char, count in t_count.items():
                    if window_count[char] < count:
                        valid = False
                        break
                
                if valid and len(window) < min_len:
                    min_len = len(window)
                    min_window = window
        
        return min_window


def demo():
    """Demonstrate Minimum Window Substring solution with test cases."""
    solution = Solution()
    
    test_cases = [
        TestCase(
            input_args=("ADOBECODEBANC", "ABC"), 
            expected="BANC",
            description="Basic case - 'BANC' contains A, B, C"
        ),
        TestCase(
            input_args=("a", "a"), 
            expected="a",
            description="Single character match"
        ),
        TestCase(
            input_args=("a", "aa"), 
            expected="",
            description="Not enough characters in s"
        ),
        TestCase(
            input_args=("ab", "b"), 
            expected="b",
            description="Single character target"
        ),
        TestCase(
            input_args=("ADOBECODEBANC", "AABC"), 
            expected="ADOBECODEBA",
            description="Target with duplicates"
        ),
        TestCase(
            input_args=("a", "b"), 
            expected="",
            description="No match possible"
        ),
        TestCase(
            input_args=("abc", "def"), 
            expected="",
            description="Completely different characters"
        ),
        TestCase(
            input_args=("AAAAAAA", "AA"), 
            expected="AA",
            description="Multiple same characters"
        ),
        TestCase(
            input_args=("wegdtzwabazduwwdysdetrrctotpcepalvzaasccoagwagzsyzgruutxnhvyzrnckdqyucdfnmiauaomhprrxydtjjzqykywajqwpgzsrsgttgvjhpaprgvdzwlqsrsdhcejhsfxcpnfseggdsdkdoffrxgqowlshlnlcbkqtsydlvdaytwcttjpqnyukdbmdgeiipslzckvoyyqwdltmzowdybytezcvlnvwsidodbdbhfxggctbhcbkchgrwamdgyxggmaaacvgfkbktjtpxyhpzapzxxjngeeepzmtwnazxjcnyrczayjtocsrcamzvkfimzezgdtdufhcrssmlzgrsnxvspyyyatvhspvejuhcglaoefkjgkzwqvdyqdxtrdkqyvfnggkobwpswjagzmhwbxcakfcqhyexjlbapxdbyehfvkqltcmidkdddctkehscrxzckpyiltoqnimgkhprbrcdfzaayzmqsgtbjccyzepbktrjfzsxvqfwzwepawgqhqnmjpckdmvqyizgmphxhqgsgwtqnfclayhtqmbdipwlpdwfskxhfqgrqrrcrvmepkxtzwcwzncevqpkdvdzbfqhbvrzjhybkkmkxgvzrohvibfzehklmkivolaafvfshowkxhvowkehwgsxjqecxdlqtpyqqvnvlhkgtutdlcndjltvbwzmtdlzddrmvazjpdpmvgpnpbahyqhcsdgzjfslhzkpjdntkgmhtyzhsyecqrfzpnhylqbmgwuaaxtedwczdshikxgwaxmftlmryamdqrpfkhmdsaxtfklwvuwdkfzkzjhxikbvhfvlumfazhqozlddsmmjqnuwjxkshqtpopfnyqnzwvjtjzrcbqoykdqpgkcenzcpuwefowlszdqhvtwafmhiwxbywjjcqhbhfpvpnwshscoyblcqfbsrxhyoibdqvgppnzakzgqyowgpvzkppktwlxyxpdatvmcavqfqsrgnbqvmjyxfozprsrlqxqxjtrlzmfqfygqkhgdaxlxzryrfkdwdqxnhbsnfqsqlfvlolnpttgrpsaqtmvscwtwppkgdvnzcbydysbjkxyksltkmgbtdrvdnruwqvdtdbbmcnowfmejdrgdwgdzkxdojnyrhkozqhqwdsqbdjbvohvobbtuxqgxrjhsbfylrplrqgbczxlgtejdlitpbgmjzjplbvhycnazawczutnkozjtgxzqgxbxwvyvqjvxfddoouiicvuvbrcykqjpawhhzcegzlqflpsdjnvggscibcbdssefgvcsadxqjowmttmcxkyvmyidgvgqklvvdvxcqkwqihdbqjbizmlkdoohxcwdxdjvgbwznkqvpffpqjltzjkwlwnbjbbfhfbtctqdehyvnbwklpumqwwsxhklprxjqfggbjylfkqbibdvrlnhvfjcycdgxbmsbfbykepivnfkspdxfhqwqtyjhyqvlmjvycpgxkuprpqoujydfrntqsjvdmgwcqjgecimjcpnstlgcngqxkvdoldfzqwsgcjzacekxnimfqcrrzlqefkpxyzgdrfnsfokzztksjkdxfvtmkzccnxkcjhkzwqvtinpgpspovknhkvzvcrvpcnjqzjjfafvnlqdvxjqovxdsmyczcttubmbgzygsjwkfqwftfavdkmdvxpjpcttphwegdqwsqzjzbrfavqhcfvzljqtsgxwsyzaqdphcntnlzqkcytfbumolmgdkqzuagzjfghllkqhvsqchmzjtzukzmlsrksatktpjrqcbjcquvgwmttbhgngxdvwmstbfqucqkktmhgpskpddbdpqljgfkxkxlhxgbhhfqhzdhocxvyfkxqlzfzwtxjdqxrhgfhkskzqsbnpvfqfkuhslfpxpfngjhjzxjwdybcnhghxqjhfyepqpfnpgrwbdcjtgkxelgsxndwlhdzgagvnvhjphzqgvpqcrtnxvlvxhqvgzfhscvhfjdgncjgjvdgrplxibuqzxqvemhkzcsvqxhpxqpgppcvhdftlbhxgjzqdxfyccrctnplzgmgfblxqkqjcrvxljhzngfvymkrhmjwhspvcgtavqfmumhtfyqfdhwehqgbvdxhgvlwcwdnjmkcgqlfmdlzjqxbwmpgtctjyuhjhqhsnswmgmjlmrjflxlnkplbxgyhcrsntlzpxizkplxjxkqlgxfchddfxjdqygbtcwejxvzxksbjhgymbagvqzecuuprnbdcswvzsyvytnxdxwvmcskgtjbddzfkgsgpqtntddvqslhzxwfvsppznssdedjjlznhklnxqhpzrmqttdgqstjbzwfvhxxqplpqvzbawzijdslbjdyxlwmwsjgggqfzkxjdkqnygmjhryqtxlwcxrvfnezxhtxzqrgnlsqdtgkrvlhldngtnqvhwqvbwjfvbpmhfgwjdqnkvbvpvppvqfdxdcfrvvvdxkttxfjbkglzpxdwqxqvaqtwcqsevqrytquvlzkejhfmtvqfhmefmgncpzfmtfbfqkrtrrkngqffkklzafnqwkffmtmsctevwegwcqjbvktrkhxbqhbxnfmspwlzrjdqrpnvnpjvlcwdtdwdbnwgvddmdxpqbdxfmjgmvdnqawfxqmhruzrbhyzjajfxncjxnfgdwyjzgmgdpqxzxtmvtdyldqnfqzlttjklrxpkxprwjpegfrdkpfntmqblgqmwtqfgbmrblufbbbrrmbxdqtrzzqtvpdnjnlvntvtqgsmtmwscdndtgwgzwdshmsbagyzphhlmjgmthuvjptxpbwacnpykwjvmxmgcgnyxzprldqmgvqhxkdhhkxlprqclwjgmzpqnxjcqzrhkzzefxjqcvdszgfqtkvlbjxgqhqzntsjnxkbgbvjjsjtdldrpztqwshwbklnhrvflyxrzqhqxjhexzpghdpgjjuxtfhlkqgnmhvpwgzwlghvtzykkdmzjrjzjdsvnwhvlqkldthzbhsxwsghdxdgrxedqjklrfzjwtdsgulvnhrdkpjpdfcxhbpdfzscqxtydytxsgckdujcrczmwbmysjrexphfbljclxkdhrjdvfvgbkdvcxlrmpmcfehzzwjrvjfnmxdzphlrbstnhwxggtgdqyvcrdqjxfbxjfbqzhytfmxswrvlzrqjpvzszdwvwlwnhdgdxlhplxdhcmvlwbtmcygzjbxqjkgqcmpncvxhrcpmttlwpmvqtdqchqbxgbqpqrhfjqbmkqzjdsmzrnxmdfhxcsvvwdjqtmcqrkkczfdrdqrwwgmfglxzqzvmhsqmtdqwfvxlzjchkgmqxdmzjyqqfqrqglswdsxwlmjlpvqnhqpzhptwqmzzxmfnjdqcfrtzlfqfmxhfrqpctfdjhfzxqxrxxfqrwzjmzzjqmcrqrldxgtrftphjkxjftqhbljvcxgpmbvfqjxvdrrlmxkbmfdjhthgzqxjfgvrwbxhvgvqdsbjmnwhlqmqqxbbdvgqgbjfnkgtgqrkvxjxkzqtdcsqrxvbplmlxtdkpnwzlmjgwqjmrjtdlzfzzvhqfmjvdmkrztdgmjfvtmzljncvzwpgtdtbjlrgrqktbtkmpngrftlzzxsvjqzgvrwgdlgrgrsqwjzlblfcfvwzrkjhdbcqltqhzlpbqnrnqgrzqpwtgsxtlcqczzqcsgwfdjzppgxjmtqrtzdzldvdpzwdlrhjzqhsrvgzzrxxjqcjfxbzhxhxpljgfvjhpqcgfxhfjkchzdzrxsjhqpgdclfkbcswhlkqrtzrkqwxxwrzwvmlgjmwqhxqdrgszqzjjhdpvvnsvfwrtfrnnkjcqmqgxqvttjmjshwpfhbgpncfldxnzlqkhtrqwjfbccwpdjcfqnjjxfrczlcvwfctkmqgflcvnfxwpxwnqjjgtbtpxbhwlqfcxqsqjrzbwcklxdnjrljxqmzmmlnmdqxzrgdqmwmjgmqjhkfvfbzcjjfdgmdslzhdrsndgvqjhsbfglqlckqjpphjtcqnwtwghpsmxjmzrkptqhccldtqfdpjqtdwsrjftxmjzqsvrpmvtplfgwqhfwcdwsbwjnpghdqhzpnqmfqrwkzwbxlglbwvgwmzjhckpvgnpxzbrjxkbngnlwrqfxlkmddqbphmkqxbdpmpcbqmbwlmmrwvgsxwscctxlvcbvjbqnwvjbdvvnjghvhdbktvhfvqdqrwtnjnmqstwmthjcltmzxpkbdtvqqxgghcswhqwsrfkqjgtrfgrctdlpmqrnzxzzzczcvnnhtwsjjdhmqnszjkdnktjrrmrjzzmdrpwfngpktdgrqcdpdbztjmbxwhlznnqcjgdmrhzjztdgvrjlpqxxwdcmcmvqcpgvxsjsqlbrqjghwxschlrmcnrwzjnqzgbdljnhsqzwgwmckmgrpqtqzjgftttmkrzvkjbhqpbdlcwgsprbvcxfdbvvpzcwgnqmplzrlqmfqsmqcdzcbslcvgtvvqvpvsmpbncnrwlvhqcnzppfjlhcdvvmwktvmjfvhqmtqkplzqhhvlblqwqmkhrjqfxmlfxqnrhlccbqvgmqnbwmjgvqgzfxtfmcglgcvtpgmxrkcqcqzfvtqjqmrjtwbdvqxzvfljdlmnlxsqgtdrjppljfflnxzkjcqjvndkxvtwgjqfbzmwqhqfplsdxmsdkfrxdjtxltmtkzxmxplpzjhqbqnpfpthwcrtnthqxtwxqhzjjlxhqfmddbzwtkdngztpgzcpkfpkwszwvmxjjnxdwktghfjqdbrfcztscglpqtqhqqlvjvdkcpxlcqbdchbhrjwclzgfwfdzjdtjmmvrfwqmxjbhvvgqbdjmnvxddlxpvfzjnhgshwtzxktjwmvgqjcgszljsgcdpfclxvfgxnvxtxhftmxgrkldjhcrcgkzwrmgbrfqxvwlqnbgwlzcqttmzzvvsjphrjhlfgpkxmsfvvqdhfwtshtzfxftcmhfwmkdnvdtrqrrvpmhqwqnbrrzwgkmkxksgcmpqfbxjjzzlwmgdvhccxbxdhlzjjhkjdzbchswgkwvqqxkbwrgtjvtbnnvkllmqkjxqpzklpzldgkcbvxjqwqpgkvlbrqchhczwlqtblphwhdkmvhgwwqzwklcbfrwmlfkpdrjsvgnfvvpvglpccdvgzcfgmlcmjddssgddcmlwmwbsxdwhfrtzfggmxlqpwlfhzvgfnmzdqzgrwkwgdlbgmwxjhzmhdmrmdklnchzqtdczvjrvpljqxlpmfnqnlghsgbqmqfwmvmsrqxlkmvfngjhqhqnpdxlxccklfrvdcswdgltwvhpxmhmsjvpzflxdqzjdwjvdwrqjgjxjqfpbssgscxzdjrxdwgqpjhqmdrjjjnnbtrglpgqzlcwblzxzqrlndckftbqssbdkqjrdrhhlhtcdzxfdsfmhkzgnxpxhrpqmlqdkhhlmqqmnhbqvgvgfhqvzlrjhmlbdvsqgczzdgjxqzcssjlgjkqhjxjdvxjdnjbzgmbbmqbdgdsmtqzklzrqxhbhbhbcxkcxpjtrkqbfqwlsqjphkrtxdrcbjkfjdqgzzmdnkmjhgckksmwtpwhzmqjgqsqcpgqxhvwklwlddmdxvhnmhkqtphdzftjzfxhgqlpjsxhxqfvdnwxwtqzjgpqtwdxmvxhbrtttfwbxpjjfrpzctmvjfnmgwgwbcbqmcdsgqxqdnjjkcvphntwjrcwqlfqmfcmpklcqlsfhvnxfrkcjqzlbrrdrmdbmgccdnjlpbpfhnlftxzckkzzjnhzwxhqjqlmwcnlqnvzptmhqtnhzsdmgvnrtqgtbvqzlwqhtdlhkgzdckwqkvbzdswlcnvdpwdrmqjsczcxfgtqwjzgpfqngvtwqwnxmkzvqslrcfggtcwqctzrcmdcthgqcrqcjdnpqtgdbgbdvcbhjfgjsrmvxjscqhgclfpxtxjgzpxgkwqvtwbqjvtdqmgqqtxdcqnvsdqccjjnhzpzlqvtqcshrtgzgzjhrfhsvjjmgnqrbxvcplzglrlgbsnvpgpmnzxqbxlvtwlqrthjtjkfcdgbtmpqzrhslqslvcvlmxhhhlnvtddgtpnwjvcqjxqwrxxcsmjjvlqrftkcthmcckrcdmxfrsmgkdgcmmnczqzkmwzqjgbbgxghncnlnxczmtcrtzsvzlbrgvwhmnhtpjlxnqczprcqrgdwhzjqnbcvkzpdtrqfwjcblwtwrrthzhtmcwjhwqqtcnqccrhrdmqhfvgdxwxqgmbwbtqdlqjsxdczlrwzmjnfzqdxbljzdbnhxlgzxmdqxqglcmgzsjvtdsvkbfqfzmlrmqdqqgktbkhqhmvnqsfhlzfhdmdnvcdjnbtqnnrlbjvswddbnbcqsqzfvckcgkfdbqhkfkjsrmvlkkplmcqnvczhfjjdztdqqhqbqwxgdqtqmrbdngtztcrwgzsmjmbkdtdmpkqzlvbcrqssjwmwqzbpgrphwrfzfbfxdszfpckrftdwfszgcxsqjwxnvjrmddzfvnwzxpjqrtxwqxsqkrjzvzltgqghxsmttxcbrhzhkdhcvqjzgvgwzqnxdnqbkqrftvmhmwzljxrcwjjjwqghhkwmjpldrxkhdjzxmvzxnhkjklsqzqfjdggjxgwxpkmnqlthmpzfgdhjxfdqzqgcczfjfdrjljzwlbqccqljqbmxqtgcxlpzmpdzcnmvlmvqmxdrtrgrnqmmpwjhtpfdlcbcrvxqjcwprzdpzcscjhgwxpdppjwmxnvpqcnwcpqgwpxmxqzptrdrmwzjmqltvkxtggxsqbbmhpxqpnfcrqmqfqhzlbmnwbcqlfrqgnlmjhgtqmjbcgvkgqtzfkqvdsbrzcrrcmwswtgjdbnsjhcrvxgzpswjmtnqdrglzhtjmjmfzcgxtdmhcnvjxhxkrddbwwjhpmdsfgqwzzvnpqqmqgdmpwmbwdhqcrxlftxwglpnfzcmfwzwcfpnbhgvqkjzpgddrmjnffpzqllndbwdnfvdjzrgsdnzmxzmlvjwdlbwdmjbxszdqghfvfzfqbjczkctqrbgpnkxfxlzrbtcvcxhrbxzdxthgqbvztvpmrcttgrnxmtgzqdqcxmcfzbrqvlmrhbqhqzbklqgfmbkglsthqknflfvdkxhzlgjdxfvwctptflgczjgfhpqrfwzjjcfjpkwqwrfwgxxmxzpgjnfbgswcgvdgxdsmhgqxkqgmtngpjlfrtnfqjxzsqrtnrcxqgmdbvgqvdrqgfqcfspzjgvvqnqmfhdfgmjwqcnfnrqtvlrrbpdcxdgckxdmdnlqvqqqhtjmkpntpmqsxzhqnbgcmvgxltwqzmwzfrwclhwnqbtwfqbclbgcltcnmvzgwvfpbgqqwpnzlqzwbqtwstllcsbxjtgcdlkgvqhqmqzxhgzjjspdmqrktrzhlrchqrdpqzmnfbxhqbxqcjgfcjrtbmpkqtrdlztzlmntwqhbtmvxfbllwczqjgqpgxdzhbtbqmclqwjhkxczrddmplmqzfzlqvdvhptkxtlgwpgkjkqhbcllptqmgzltldzzxcgjpxrljxkrhpqsnrmxtpbwbqzrhmfpjlklscbkglhfdmctznjpzxzpqkcgzqhtrxrxqjrdbbkdplznnvdqjqmqgmxdvnfcjqmnqjbjjjprdpbvvqpdxqqqrwvrxdbfnclzmtmqbnxkqtttkdnbbttmwdsjzrfvcqjjhqjztxpkdngzhvvndfbzfkpzwmnjqsqzvfqrqhxdxztllcfjznjrncdhmxkgvqwsrbqsmkdztgvktdnftqjmlxnxtncwjqdqmhvfgmqxbxxhgdqlbpgvdhzqzxvrmkmzjqssfzkcnfnrwqwjqvlhqxdmpzmkdlftqgpptrszwnfpntlbwfkcfwlsljjdptjdpnfjzhdjbrpfgtsmmxmjvsqfbfjckgdhlmkxsqrhjkjrsmfhqprrmhqhmrlqjfzlhvphdqtvdjdqbhppnzlvfrjqkgpmxbhqvqlqgcpgqzbrbnvnhvnswqrvjhfscqpkqmjdwlcpxddxqsccmkcnctrxdmqfqrtfqpgbbjlqbqglqdcchjcbldwlphgwsfgmptwlqfrmdjgvwwgttzqgzxfxdwphjnxdgnqgljzjlvtlkrdmbrnncdlqdjzppnxkgbmxkdgkztqpjdwlgpxpctxgrqzjhvmfqssnhvqsqbqjjgwdsgdgcfvdwxdhtqzlhzzrnrrxhpjkzhrlqghmmxgmndhqmkggrmnbvlttnqkqrqmrpqzzkrqthqfpcrcpjhbfvmjmjqzglzglfrwghmhfrqvnpqhxkbcdbcqjgpmwfjcztvnscpczvhzhgccgglhvsgtpmfztrlnkwqbqdkcrthqwjgshcfcvspgpnrqxkzxmrxrcdqvqnlbxnlzqf
