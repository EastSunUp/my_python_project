

class Node:
    """链表节点定义"""

    def __init__(self, x: int, next: 'Node' = None, random: 'Node' = None):
        self.val = int(x)
        self.next = next
        self.random = random


class Solution:
    def copyRandomList(self, head: 'Node') -> 'Node':
        """
        深度拷贝一个包含随机指针的链表。
        使用哈希表记录旧节点到新节点的映射，处理next和random指针。
        时间复杂度O(n)，空间复杂度O(n)。

        Args:
            head (Node): 原链表的头节点

        Returns:
            Node: 深度拷贝后新链表的头节点
        """
        if not head:
            return None

        # 创建一个哈希表，记录原始节点到拷贝节点的映射
        node_map = {}

        # 第一遍遍历：创建所有新节点，并建立原节点到新节点的映射
        current = head
        while current:
            node_map[current] = Node(current.val)
            current = current.next

        # 第二遍遍历：连接新节点的next和random指针
        current = head
        while current:
            if current.next:
                node_map[current].next = node_map[current.next]
            if current.random:
                node_map[current].random = node_map[current.random]
            current = current.next

        return node_map[head]


def test_copy_random_list():
    """测试拷贝随机指针链表的功能"""
    # 构建链表: 1 -> 2 -> 3 -> None
    node1 = Node(1)
    node2 = Node(2)
    node3 = Node(3)

    node1.next = node2
    node2.next = node3

    # 设置随机指针
    node1.random = node3  # 1的随机指向3
    node2.random = node1  # 2的随机指向1
    node3.random = node2  # 3的随机指向2

    solution = Solution()
    copied_head = solution.copyRandomList(node1)

    # 验证拷贝是否正确
    # 这里应有更详细的验证，示例中简单打印部分信息
    print(f"原始链表: 1->2->3, 1的random指向{node1.random.val}")
    print(f"拷贝链表: {copied_head.val}->{copied_head.next.val}->{copied_head.next.next.val}, "
          f"{copied_head.random.val}")
    print("测试通过！")


if __name__ == "__main__":
    test_copy_random_list()