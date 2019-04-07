#include "mplist.h"

#pragma region 构造函数

MPList::MPList()
{
	head_ptr = tail_ptr = nullptr;
	length = 0;
	var_name = '\0';
}

#pragma endregion

#pragma region 析构函数

MPList::~MPList()
{
	for (size_t i = 0; i < length; i++)
	{
		DeleteFirst();
	}
}
#pragma endregion

#pragma region 可读属性

MPNode* MPList::GetHead() const
{
	return head_ptr;
};

MPNode* MPList::GetTail() const
{
	return tail_ptr;
}

size_t MPList::GetLength() const
{
	return length;
}

size_t MPList::GetVarNums() const
{
	return GetDepth();
}

char MPList::GetVarName() const
{
	return var_name;
}

bool MPList::IsEmpty() const
{
	return length == 0;
}

size_t MPList::GetDepth() const
{
	return size_t();
}

string MPList::ToString()
{
	return string();
}

#pragma endregion

#pragma region 重载运算符

MPList* operator*(const MPList& l_list, const MPList& r_list)
{
	if (l_list.IsEmpty() || r_list.IsEmpty())
	{
		return nullptr;
	}

	MPList retVal;

	l_list.ForEachC([&](const MPNode & a)
		{
			r_list.ForEachC([&](const MPNode & b)
				{
					// 两个表的每个节点都和对方的每个节点相乘一次后插入新表
					MPNode result = a * b;
					retVal.InsertFirst(result);
				});
		});
	return NULL;
}

MPList* operator*(const MPList& list, float coef)
{
	if (list.IsEmpty())
	{
		return nullptr;
	}


	MPList retVal;

	list.ForEachC([&](const MPNode & node)
		{
			// 系数与表的每个节点相乘后插入新表
			auto result = node * coef;
			retVal.InsertFirst(result);
		}
	);
	return NULL;
}

MPList* operator*(float, const MPList&)
{
	return NULL;
}

MPList* operator+(const MPList& l_list, const MPList& r_list)
{
	if (l_list.var_name != r_list.var_name)
		return NULL;

}

MPList* operator+(const MPList&, float)
{
	return nullptr;
}

MPList* operator+(float, const MPList&)
{
	return nullptr;
}

ostream& operator<<(ostream& out, MPList& in)
{
	//out << in.ToString();
	return out;
}

istream& operator>>(istream& in, MPList& out)
{
	//string temp;
	//in >> temp;
	//out.FromString(temp);
	return in;
}

#pragma endregion

#pragma region 成员函数
void MPList::FromString(string s)
{

}

void MPList::ForEachC(function<void(const MPNode&)> func) const
{
	MPNode* cur_node = head_ptr;
	while (cur_node != nullptr)
	{
		func(*cur_node);
		cur_node = cur_node->tp;
	}
}

void MPList::ForEach(function<void(MPNode&)> func)
{
	MPNode* cur_node = head_ptr;
	while (cur_node != nullptr)
	{
		func(*cur_node);
		cur_node = cur_node->tp;
	}
}



//MPList* MPList::Copy()
//{
//	MPList* retVal = new MPList;
//
//	ForEachC([&](const MPNode & node)
//		{
//			MPNode* new_node = new MPNode;
//			// 使用节点结构体默认的浅拷贝构造函数完成浅拷贝
//			*new_node = node;
//			// 对于含有广义表的节点对广义表也进行拷贝
//			if (node.elem_tag == LIST)
//			{
//				new_node->list = node.list->Copy();
//			}
//			retVal->InsertEnd(*new_node); // 因为ForEachC 是顺序遍历的，所以赋值得使用尾插法
//		});
//
//	return retVal;
//}



bool MPList::InsertFirst(MPNode node)
{
	size_t success_counter = 0;
	// 为了化简，当遍历表上存在的所有节点，当指数域相同时，需要对“系数部分(含多项式广义表)”相加
	ForEach([&](MPNode & iter_node)
		{
			if (node.exp == iter_node.exp)
			{
				// 相加有三种情况：
				// 1. 系数和系数相加
				// 2. 系数和广义表相加
				// 3. 广义表和广义表相加
				if (node.elem_tag == COEF && iter_node.elem_tag == COEF)
				{
					iter_node.coef += node.coef;
				}
				else
				{
					MPList* temp_ptr = nullptr;

					if (node.elem_tag == LIST && iter_node.elem_tag == LIST)
					{
						temp_ptr = (*node.list_ptr) + (*iter_node.list_ptr);
					}
					else if (node.elem_tag == COEF)
					{
						temp_ptr = node.coef + (*iter_node.list_ptr);
					}
					else // if(iter_node.elem_tag == COEF)
					{
						temp_ptr = (*node.list_ptr) + iter_node.coef;
					}

					if (iter_node.list_ptr != nullptr)
					{
						delete iter_node.list_ptr;
						iter_node.list_ptr = nullptr;
					}
					iter_node.list_ptr = temp_ptr;
				}
				++success_counter;
			}
		});

	// 动态分配一个节点，浅拷贝形参
	MPNode* new_node = new MPNode;
	*new_node = node;

	if (head_ptr == nullptr)
	{
		head_ptr = tail_ptr = new_node;
	}
	else
	{
		new_node->tp = head_ptr;
		head_ptr = new_node;
	}
	++length;
	return true;
}

bool MPList::InsertEnd(MPNode node)
{
	// 动态分配一个节点，浅拷贝形参
	MPNode* new_node = new MPNode;
	*new_node = node;
	if (tail_ptr == nullptr)
	{
		tail_ptr = head_ptr = new_node;
	}
	else
	{
		tail_ptr->tp = new_node;
		new_node->tp = nullptr;
	}
	++length;
	return true;
}

bool MPList::DeleteFirst()
{
	if (head_ptr == nullptr)
		return false;
	else
	{
		auto next_ptr = head_ptr->tp;
		if (head_ptr->elem_tag == LIST)
		{
			// 帮节点回收广义表对象的内存
			delete head_ptr->list_ptr;
		}
		delete head_ptr;
		head_ptr = next_ptr;
		--length;
	}
	return true;
}
#pragma endregion
