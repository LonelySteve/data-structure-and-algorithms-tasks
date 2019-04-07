#include "mplist.h"

#pragma region ���캯��

MPList::MPList()
{
	head_ptr = tail_ptr = nullptr;
	length = 0;
	var_name = '\0';
}

#pragma endregion

#pragma region ��������

MPList::~MPList()
{
	for (size_t i = 0; i < length; i++)
	{
		DeleteFirst();
	}
}
#pragma endregion

#pragma region �ɶ�����

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

#pragma region ���������

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
					// �������ÿ���ڵ㶼�ͶԷ���ÿ���ڵ����һ�κ�����±�
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
			// ϵ������ÿ���ڵ���˺�����±�
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

#pragma region ��Ա����
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
//			// ʹ�ýڵ�ṹ��Ĭ�ϵ�ǳ�������캯�����ǳ����
//			*new_node = node;
//			// ���ں��й����Ľڵ�Թ����Ҳ���п���
//			if (node.elem_tag == LIST)
//			{
//				new_node->list = node.list->Copy();
//			}
//			retVal->InsertEnd(*new_node); // ��ΪForEachC ��˳������ģ����Ը�ֵ��ʹ��β�巨
//		});
//
//	return retVal;
//}



bool MPList::InsertFirst(MPNode node)
{
	size_t success_counter = 0;
	// Ϊ�˻��򣬵��������ϴ��ڵ����нڵ㣬��ָ������ͬʱ����Ҫ�ԡ�ϵ������(������ʽ�����)�����
	ForEach([&](MPNode & iter_node)
		{
			if (node.exp == iter_node.exp)
			{
				// ��������������
				// 1. ϵ����ϵ�����
				// 2. ϵ���͹�������
				// 3. �����͹�������
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

	// ��̬����һ���ڵ㣬ǳ�����β�
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
	// ��̬����һ���ڵ㣬ǳ�����β�
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
			// ��ڵ���չ���������ڴ�
			delete head_ptr->list_ptr;
		}
		delete head_ptr;
		head_ptr = next_ptr;
		--length;
	}
	return true;
}
#pragma endregion
