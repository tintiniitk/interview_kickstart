from dataclasses import dataclass


@dataclass
class Item:
    Name: str
    Weight: int
    Value: int

    def __str__(self):
        return f"{{{self.Name},w={self.Weight},v={self.Value}}}"

    def __repr__(self):
        return self.__str__()


Items = list[Item]


class Solution:
    def __init__(self):
        self.max_value_so_far = 0
        self.max_value_back_packs = list[list[str]]()

    def helper(
        self,
        items: Items,
        nextItemIndex: int,
        slate: Items,
        weight_limit: int,
        weight_so_far: int,
        value_so_far: int,
        final: bool,
    ):
        # print(
            # f"{'.'*nextItemIndex}helper(max={self.max_value_so_far}, slate={[item.Name for item in slate]}, items={items[nextItemIndex:] if nextItemIndex < len(items) else []}, weight_so_far={weight_so_far}, value_so_far={value_so_far}, final={final}"
        # )
        if final:
            if value_so_far >= self.max_value_so_far:
                new_combination = [item.Name for item in slate]
                if value_so_far > self.max_value_so_far:
                    self.max_value_so_far = value_so_far
                    self.max_value_back_packs = []
                self.max_value_back_packs.append(new_combination)
            return
        nextItem = items[nextItemIndex]
        # include next
        new_weight = weight_so_far + nextItem.Weight
        if new_weight <= weight_limit:
            slate.append(nextItem)
            self.helper(
                items,
                nextItemIndex + 1,
                slate,
                weight_limit,
                new_weight,
                value_so_far + nextItem.Value,
                new_weight == weight_limit or nextItemIndex >= len(items) - 1,
            )
            slate.pop()
        # exclude next
        self.helper(
            items,
            nextItemIndex + 1,
            slate,
            weight_limit,
            weight_so_far,
            value_so_far,
            nextItemIndex >= len(items) - 1,
        )

    def fill_sack(self, items: Items, weight_limit: int) -> tuple[int, list[list[str]]]:
        self.helper(
            items,
            0,
            Items(),
            weight_limit,
            0,
            0,
            False,
        )
        return self.max_value_so_far, self.max_value_back_packs


if __name__ == "__main__":
    items = [
        Item("macbook", 2, 2),
        Item("iphone", 2, 3),
        Item("jewellery", 4, 5),
        Item("watch", 1, 2),
        Item("luxury_bag", 1, 2),
    ]
    s = Solution()
    max_weight = s.fill_sack(items, 5)
    print(f"max_weight({items}) = {max_weight}")
