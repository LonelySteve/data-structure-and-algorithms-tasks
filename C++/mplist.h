#pragma once
#include <string>
#include <functional>
#include "mpnode.h"


using namespace std;

// 广义表类(本质上是一个单向链表)

class MPList
{
public:
	// 构造函数
	MPList();
	// 构造函数
	// MPList(string);
	// 析构函数
	~MPList();
	// 获取多项式广义表的长度
	size_t GetLength() const;
	// 获取多项式广义表的深度
	size_t GetDepth() const;
	// 获取多项式广义表是否为空表
	bool IsEmpty() const;
	// 获取多项式广义表的表头节点，空表头返回nullptr
	MPNode* GetHead() const;
	// 获取多项式广义表的表尾节点，空表尾返回nullptr
	MPNode* GetTail() const;
	// 获取变元个数
	size_t GetVarNums() const;
	// 获取当前多项式广义表的顶级变元名
	char GetVarName() const;
	// 头插节点（相同指数项将自动合并）
	bool InsertFirst(MPNode);
	// 尾插节点（相同指数项将自动合并）
	bool InsertEnd(MPNode);
	// 头删节点
	bool DeleteFirst();
	// 相乘两个多项式广义表
	friend MPList* operator *(const MPList&, const MPList&);
	// 多项式广义表和系数相乘
	friend MPList* operator *(const MPList&, float);
	friend MPList* operator *(float, const MPList&);
	// 广义表和广义表相加
	friend MPList* operator +(const MPList&, const MPList&);
	// 广义表和系数相加
	friend MPList* operator +(const MPList&, float);
	friend MPList* operator +(float, const MPList&);
	// 获取字符串表示
	string ToString();
	// 从字符串表示初始化多项式广义表
	void FromString(string);
	// 不递归地用指定处理函数遍历子节点（不允许修改节点）
	void ForEachC(function<void(const MPNode&)>) const;
	// 不递归地用指定处理函数遍历子节点（允许修改节点）
	void ForEach(function<void(MPNode&)>);
	// 重载输入输出符
	friend ostream& operator <<(ostream&, MPList&);
	friend istream& operator >>(istream&, MPList&);

private:
	MPNode* head_ptr;
	MPNode* tail_ptr;
	size_t length;
	char var_name;
};

